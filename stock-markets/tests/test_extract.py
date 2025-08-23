from configs.yahoo_finance_client import YahooFinanceClient
from elt.extract import Extract
from tests.test_config import TestConfig

test_config = TestConfig()
client = YahooFinanceClient(test_config.config)
extract = Extract(client)
ticker = client.fetch_ticker("AAPL")

def test_extract_stock_data_by_period():
    df = extract.extract_stock_prices_by_period(ticker)
    assert df is not None
    assert len(df) > 0

def test_extract_stock_data_by_date():
    df = extract.extract_stock_prices_by_date(ticker)
    assert df is not None
    assert len(df) > 0
