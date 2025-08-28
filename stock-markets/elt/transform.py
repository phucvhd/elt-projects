from pandas import DataFrame
from yfinance import Ticker

from elt.configs.base_model import StockPrice, Dividend, StockSplit, CorporateAction, TickerInfo
from elt.configs.mapper import Mapper


class Transform:
    def __init__(self, mapper: Mapper):
        self.mapper = mapper

    def transform_ticker_history_to_stock_price(self, df: DataFrame) -> list[StockPrice]:
        try:
            print("Transforming ticker history to stock prices")
            return self.mapper.map_stock_price(df)
        except Exception as e:
            print("Error when transforming ticker history to stock prices", e)
            raise e
            
    def transform_ticker_to_ticker_info(self, ticker: Ticker) -> TickerInfo:
        try:
            print("Transforming ticker to ticker info")
            return self.mapper.map_info(ticker)
        except Exception as e:
            print("Error when transforming ticker to ticker info", e)
            raise e

    def transform_ticker_to_dividends(self, ticker: Ticker) -> list[Dividend]:
        try:
            print("Transforming ticker to dividends")
            return self.mapper.map_dividends(ticker)
        except Exception as e:
            print("Error when transforming ticker to dividends", e)
            raise e

    def transform_ticker_to_stock_splits(self, ticker: Ticker) -> list[StockSplit]:
        try:
            print("Transforming ticker to stock splits")
            return self.mapper.map_splits(ticker)
        except Exception as e:
            print("Error when transforming ticker to stock splits", e)
            raise e

    def transform_ticker_to_corporate_action(self, ticker: Ticker) -> list[CorporateAction]:
        try:
            print("Transforming ticker to corporate actions")
            return self.mapper.map_corporate_actions(ticker)
        except Exception as e:
            print("Error when transforming ticker to corporate actions", e)
            raise e
