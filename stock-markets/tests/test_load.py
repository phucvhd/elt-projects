import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.base_model import Base
from configs.repository import Repository
from configs.yahoo_finance_client import YahooFinanceClient
from elt.extract import Extract
from elt.load import Load
from tests.test_config import TestConfig

test_config = TestConfig()
repository = Repository(test_config.config)
client = YahooFinanceClient(test_config.config)
extract = Extract(client)
load = Load(repository)
ticker = extract.extract_ticker("AAPL")

# @pytest.fixture
# def session():
#     engine = create_engine("sqlite:///:memory:")
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     yield session
#     session.close()

def test_load_ticker():
    load.load_ticker(ticker)

def test_load_stock_prices():
    data = extract.extract_stock_prices_by_period(ticker, "2mo", "1d")
    load.load_stock_prices(data)

def test_load_stock_prices_by_date():
    data = extract.extract_stock_prices_by_date(ticker, "2024-01-01", "2024-02-01")
    load.load_stock_prices(data)

