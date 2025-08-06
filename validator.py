import pandas as pd
from sqlalchemy import func
from database import SessionLocal, StockDailyData


def validate_data_completeness():
    """
    验证数据的完整性。
    - 统计每个交易日的数据条数，检查是否有明显缺失。
    """
    print("\n--- 开始数据完整性校验 ---")
    session = SessionLocal()
    try:
        # 查询每个日期的数据记录数
        query_result = (
            session.query(StockDailyData.日期, func.count(StockDailyData.id))
            .group_by(StockDailyData.日期)
            .order_by(StockDailyData.日期.desc())
            .limit(10)  # 只显示最近10个交易日的情况
            .all()
        )

        if not query_result:
            print("数据库中没有数据可供校验。")
            return

        print("最近10个交易日的数据记录数:")
        df = pd.DataFrame(query_result, columns=['日期', '记录数'])
        print(df.to_string(index=False))

        # A股市场股票数量在5000左右，如果记录数远低于这个值，可能存在问题
        avg_count = df['记录数'].mean()
        if avg_count < 4000:
            print("\n[警告] 平均每日记录数偏低，可能存在数据缺失！")
        else:
            print("\n[正常] 每日记录数在正常范围内。")

    except Exception as e:
        print(f"校验过程中发生错误: {e}")
    finally:
        session.close()


def validate_data_integrity():
    """
    验证数据的完整性/准确性。
    - 检查是否存在 '最高价 < 最低价' 的异常情况。
    """
    print("\n--- 开始数据值正确性校验 ---")
    session = SessionLocal()
    try:
        # 查询是否存在异常数据
        invalid_data_count = (
            session.query(StockDailyData)
            .filter(StockDailyData.最高 < StockDailyData.最低)
            .count()
        )

        if invalid_data_count > 0:
            print(f"[错误] 发现 {invalid_data_count} 条 '最高价 < 最低价' 的异常数据！")
        else:
            print("[正常] 未发现 '最高价 < 最低价' 的异常数据。")

    except Exception as e:
        print(f"校验过程中发生错误: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    print("开始执行数据校验脚本...")
    validate_data_completeness()
    validate_data_integrity()
    print("\n数据校验完成。")