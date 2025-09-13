from configs.yahoo_finance_client import YahooFinanceClient
from tests.test_config import TestConfig

test_config = TestConfig()
client = YahooFinanceClient(test_config.config)

TICKER_AAPL = "AAPL"

def test_fetch_ticker():
    ticker = client.fetch_ticker(TICKER_AAPL)
    assert ticker.ticker == TICKER_AAPL

def test_fetch_stock_data_by_period():
    ticker = client.fetch_ticker(TICKER_AAPL)
    df = client.fetch_stock_prices_by_period(ticker)
    assert len(df) > 0, "DataFrame is empty but should not be"

def test_fetch_stock_data_by_date():
    ticker = client.fetch_ticker(TICKER_AAPL)
    df = client.fetch_stock_prices_by_date(ticker, "2025-01-01", "2025-12-31")
    assert len(df) > 0, "DataFrame is empty but should not be"

def test_fetch_stock_data_by_date_ticker_not_found():
    ticker = client.fetch_ticker("APPL")
    df = client.fetch_stock_prices_by_date(ticker, "2025-01-01", "2025-12-31")
    assert len(df) == 0, "DataFrame is not empty but should not be"
