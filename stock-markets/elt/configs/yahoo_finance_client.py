import yfinance as yf
from pandas.core.frame import DataFrame
from yfinance import Ticker

from elt.configs.config import Config

class YahooFinanceClient:
    def __init__(self, config: Config):
        self.config = config

    def fetch_ticker(self, ticker) -> Ticker:
        try:
            return yf.Ticker(ticker)
        except Exception as e:
            print(f"Error when fetch ticker: {ticker}", e)
            raise e

    def fetch_stock_prices_by_period(self, ticker: Ticker, period=None, interval=None) -> DataFrame:
        try:
            period = self.config.YFINANCE_PERIOD if not period else period
            interval = self.config.YFINANCE_INTERVAL if not interval else interval

            df = ticker.history(period=period, interval=interval)
            df.reset_index(inplace=True)
            df['Ticker'] = ticker.ticker  # Add ticker column for identification
            return df
        except Exception as e:
            print("Error when fetch stock data", e)
            raise e

    def fetch_stock_prices_by_date(self, ticker: Ticker, start, end) -> DataFrame:
        try:
            df = ticker.history(start=start, end=end)
            df.reset_index(inplace=True)
            df['Ticker'] = ticker.ticker  # Add ticker column for identification
            return df
        except Exception as e:
            print("Error when fetch stock data", e)
            raise e