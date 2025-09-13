from pandas.core.interchange.dataframe_protocol import DataFrame
from yfinance import Ticker

from configs.mapper import Mapper
from configs.yahoo_finance_client import YahooFinanceClient


class Extract:
    def __init__(self, client: YahooFinanceClient):
        self.client = client
        self.mapper = Mapper()

    def extract_ticker(self, ticker_symbol):
        try:
            print(f"Extracting ticker: {ticker_symbol}")
            return self.client.fetch_ticker(ticker_symbol)
        except Exception as e:
            print(f"Error when extracting ticker: {ticker_symbol}", e)
            exit(1)

    def extract_stock_prices_by_period(self, ticker: Ticker, period=None, interval=None) -> DataFrame:
        try:
            print(f"Extracting stock prices by period from ticker: {ticker.ticker}")
            return self.client.fetch_stock_prices_by_period(ticker, period, interval)
        except Exception as e:
            print("Error when extracting data", e)
            exit(1)

    def extract_stock_prices_by_date(self, ticker: Ticker, start="2023-01-01", end="2023-12-31") -> DataFrame:
        try:
            print(f"Extracting stock prices by date from ticker: {ticker.ticker}, start: {start}, end: {end}")
            return self.client.fetch_stock_prices_by_date(ticker, start, end)
        except Exception as e:
            print("Error when extracting data", e)
            exit(1)

