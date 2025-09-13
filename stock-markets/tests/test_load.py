from configs.repository import Repository
from configs.yahoo_finance_client import YahooFinanceClient
from elt.extract import Extract
from elt.load import Load
from elt.transform import Transform
from tests.test_config import TestConfig

test_config = TestConfig()
repository = Repository(test_config.config)
client = YahooFinanceClient(test_config.config)
extract = Extract(client)
transform = Transform(test_config.mapper, test_config.config)
load = Load(repository)
ticker = extract.extract_ticker("AAPL")

def test_load_ticker():
    load.load_ticker(ticker)

def test_load_stock_prices():
    history = extract.extract_stock_prices_by_period(ticker, "2mo", "1d")
    prices = transform.transform_ticker_history_to_stock_price(history)
    load.load_stock_prices(prices)

def test_load_stock_prices_by_date():
    history = extract.extract_stock_prices_by_date(ticker, "2024-01-01", "2024-02-01")
    prices = transform.transform_ticker_history_to_stock_price(history)
    load.load_stock_prices(prices)

