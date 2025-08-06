import os
from sqlalchemy import (create_engine, Column, Integer, String, Float, Date,
                        UniqueConstraint)
from sqlalchemy.orm import sessionmaker, declarative_base

# 定义数据库文件路径
DB_FILE = "stock_daily_data.db"
# 创建数据库引擎。'echo=False'表示在运行时不打印SQL语句
engine = create_engine(f'sqlite:///{DB_FILE}', echo=False)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建一个ORM模型的基础类
Base = declarative_base()


class StockDailyData(Base):
    """
    A股日频行情数据 ORM 模型
    """
    __tablename__ = 'stock_daily_data'

    id = Column(Integer, primary_key=True, index=True)
    日期 = Column(Date, nullable=False)
    股票代码 = Column(String, nullable=False)
    开盘 = Column(Float)
    收盘 = Column(Float)
    最高 = Column(Float)
    最低 = Column(Float)
    成交量 = Column(Integer)
    成交额 = Column(Float)
    振幅 = Column(Float)
    涨跌幅 = Column(Float)
    涨跌额 = Column(Float)
    换手率 = Column(Float)

    # 创建一个联合唯一约束，确保同一支股票在同一天只有一条记录
    __table_args__ = (UniqueConstraint('日期', '股票代码', name='_date_code_uc'),)

    def __repr__(self):
        return (f"<StockDailyData(日期='{self.日期}', 股票代码='{self.股票代码}', "
                f"收盘='{self.收盘}')>")


def init_db():
    """
    初始化数据库，如果表不存在则创建表。
    """
    print("正在初始化数据库...")
    # Base.metadata.drop_all(bind=engine) # 如果需要，可以取消注释以删除所有表
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成。")


if __name__ == '__main__':
    # 当直接运行此文件时，会执行初始化数据库的操作
    init_db()