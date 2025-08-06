import akshare as ak
import pandas as pd
from typing import List, Optional


def get_all_a_stock_codes() -> Optional[List[str]]:
    """
    获取所有A股的股票代码列表。

    Returns:
        Optional[List[str]]: 股票代码列表，如果获取失败则返回None。
    """
    try:
        print("正在获取所有A股股票代码...")
        stock_df = ak.stock_zh_a_spot_em()
        codes = stock_df['代码'].tolist()
        print(f"成功获取 {len(codes)} 支A股股票代码。")
        return codes
    except Exception as e:
        print(f"获取股票代码列表失败: {e}")
        return None


def fetch_stock_daily_data(code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取单只股票的日频历史行情数据。

    Args:
        code (str): 股票代码
        start_date (str): 开始日期，格式 'YYYYMMDD'
        end_date (str): 结束日期，格式 'YYYYMMDD'

    Returns:
        Optional[pd.DataFrame]: 包含行情数据的DataFrame，如果获取失败则返回None。
    """
    try:
        stock_df = ak.stock_zh_a_hist(symbol=code,
                                      period="daily",
                                      start_date=start_date,
                                      end_date=end_date,
                                      adjust="")  # 获取不复权的数据
        if stock_df.empty:
            return None

        # akshare返回的列名可能与我们的模型不完全一致，我们只选择需要的列
        required_columns = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额',
                            '换手率']
        stock_df = stock_df[required_columns]
        stock_df['股票代码'] = code
        stock_df['日期'] = pd.to_datetime(stock_df['日期']).dt.date

        return stock_df
    except Exception as e:
        print(f"获取股票 {code} 数据失败: {e}")
        return None