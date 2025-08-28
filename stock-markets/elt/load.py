import logging

from yfinance import Ticker

from elt.configs.base_model import StockPrice, TickerInfo
from elt.configs.mapper import Mapper
from elt.configs.repository import Repository

logger = logging.getLogger(__name__)

class Load:
    def __init__(self, repository: Repository):
        self.repository = repository

    def load_ticker(self, ticker: Ticker):
        try:
            print(f"Loading stock data from ticker: {ticker.ticker}")
            with self.repository.session.begin():
                self.repository.session.merge(Mapper.map_info(ticker))
                self.repository.session.flush()

                self.repository.session.add_all(Mapper.map_history(ticker))
                self.repository.session.add_all(Mapper.map_dividends(ticker))
                self.repository.session.add_all(Mapper.map_splits(ticker))
                self.repository.session.add_all(Mapper.map_corporate_actions(ticker))

                self.repository.session.commit()
        except Exception as e:
            if 'unique constraint' not in str(e.args):
                print(f"Error when loading ticker: {ticker.ticker}", e)
                self.repository.session.rollback()
                raise e

    def load_ticker_info(self, ticker_info: TickerInfo):
        try:
            print(f"Loading ticker info from ticker: {ticker_info.symbol}")
            with self.repository.session.begin():
                self.repository.session.merge(ticker_info)
                self.repository.session.commit()
        except Exception as e:
            print(f"Error when loading ticker: {ticker_info.symbol}", e)
            self.repository.session.rollback()
            raise e

    def load_stock_prices(self, data: list[StockPrice]):
        try:
            print(f"Loading stock price to database")
            with self.repository.session.begin():
                for sp in data:
                    self.repository.session.merge(sp)
            print(f"Load stock price to database successfully")
        except Exception as e:
            print(f"Failed to load stock price into database", e)
            if 'unique constraint' not in str(e.args):
                print(f"Error when loading stock price", e)
                self.repository.session.rollback()
                raise e