from configs.config import Config
from configs.yahoo_finance_client import YahooFinanceClient
from elt.extract import Extract

config = Config()

class TestConfig:
    def __init__(self):
        self.config = config
