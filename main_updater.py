import os
import argparse
from datetime import datetime, timedelta
from sqlalchemy import func
from tqdm import tqdm

from database import SessionLocal, StockDailyData, init_db, DB_FILE
from data_fetcher import get_all_a_stock_codes, fetch_stock_daily_data

# 更新或恢复股票数据
def update_data(full_restore: bool = False):
    session = SessionLocal()

    # 确定日期范围
    if full_restore:
        print("开始全量恢复模式...")
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            print(f"已删除旧数据库文件: {DB_FILE}")
        init_db()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
    else:
        print("开始增量更新模式...")
        # 查询数据库中已有的最新日期
        latest_date_in_db = session.query(func.max(StockDailyData.日期)).scalar()

        if latest_date_in_db:
            start_date = latest_date_in_db + timedelta(days=1)
            print(f"数据库中最新数据日期为: {latest_date_in_db.strftime('%Y-%m-%d')}")
        else:
            print("数据库为空，将获取近一年的数据。")
            start_date = datetime.now() - timedelta(days=365)

        end_date = datetime.now()

    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')

    if start_date > end_date:
        print("数据已是最新，无需更新。")
        session.close()
        return

    print(f"数据更新范围: {start_date_str} 到 {end_date_str}")

    # 获取数据并存入数据库
    stock_codes = get_all_a_stock_codes()
    if not stock_codes:
        print("无法获取股票列表，程序退出。")
        session.close()
        return

    total_codes = len(stock_codes)
    commit_batch_size = 50

    try:
        with tqdm(total=total_codes, desc="更新进度") as pbar:
            for i, code in enumerate(stock_codes):
                pbar.set_postfix_str(f"正在处理 {code}")
                df = fetch_stock_daily_data(code, start_date_str, end_date_str)

                if df is not None and not df.empty:
                    # 将DataFrame转换为字典列表
                    records = df.to_dict('records')
                    # 高效批量插入
                    session.bulk_insert_mappings(StockDailyData, records)

                # 批量提交
                if (i + 1) % commit_batch_size == 0:
                    session.commit()

                pbar.update(1)

        session.commit()  # 提交剩余的记录
        print("\n数据更新完成！")

    except Exception as e:
        print(f"\n在处理过程中发生错误: {e}")
        print("正在回滚事务...")
        session.rollback()
    finally:
        session.close()
        print("数据库会话已关闭。")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A股日频行情数据更新器")
    parser.add_argument(
        '--full-restore',
        action='store_true',
        help='执行全量恢复，删除现有数据并重新获取近一年数据。'
    )
    args = parser.parse_args()

    update_data(full_restore=args.full_restore)