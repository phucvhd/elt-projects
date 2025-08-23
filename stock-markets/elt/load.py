import logging

from yfinance import Ticker

from configs.base_model import StockPrice
from configs.mapper import Mapper
from configs.repository import Repository

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
                print(f"Error when load ticker: {ticker.ticker}", e)
                self.repository.session.rollback()
                exit(1)

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
                print(f"Error when load stock price", e)
                self.repository.session.rollback()
                exit(1)