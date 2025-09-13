from pandas import DataFrame

from configs.base_model import StockPrice
from configs.config import Config
from configs.mapper import Mapper


class Transform:
    def __init__(self, mapper: Mapper, config: Config):
        self.mapper = mapper
        self.config = config

    def transform_ticker_history_to_stock_price(self, df: DataFrame) -> list[StockPrice]:
        try:
            print("Transforming ticker history to stock prices")
            return self.mapper.map_stock_price(df)
        except Exception as e:
            print("Error when transform ticker history to stock prices", e)
            exit(1)