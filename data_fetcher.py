import akshare as ak
import pandas as pd
from typing import List, Optional

# 获取所有A股的股票代码列表
def get_all_a_stock_codes() -> Optional[List[str]]:
    try:
        print("正在获取所有A股股票代码...")
        stock_df = ak.stock_zh_a_spot_em()
        codes = stock_df['代码'].tolist()
        print(f"成功获取 {len(codes)} 支A股股票代码。")
        return codes
    except Exception as e:
        print(f"获取股票代码列表失败: {e}")
        return None

# 获取单只股票的日频历史行情数据
def fetch_stock_daily_data(code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    try:
        stock_df = ak.stock_zh_a_hist(symbol=code,
                                      period="daily",
                                      start_date=start_date,
                                      end_date=end_date,
                                      adjust="")  # 获取不复权的数据
        if stock_df.empty:
            return None

        required_columns = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额',
                            '换手率']
        stock_df = stock_df[required_columns]
        stock_df['股票代码'] = code
        stock_df['日期'] = pd.to_datetime(stock_df['日期']).dt.date

        return stock_df
    except Exception as e:
        print(f"获取股票 {code} 数据失败: {e}")
        return None