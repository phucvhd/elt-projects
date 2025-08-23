from configs.config import Config
from configs.mapper import Mapper
from configs.yahoo_finance_client import YahooFinanceClient
from elt.extract import Extract

class TestConfig:
    def __init__(self):
        self.config = Config()
        self.mapper = Mapper()
