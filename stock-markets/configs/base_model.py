from sqlalchemy import Column, func, Integer, String, BigInteger, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# --- Company profile (get_info)
class TickerInfo(Base):
    __tablename__ = "ticker_info"

    symbol = Column(String, primary_key=True, index=True)
    short_name = Column(String)
    long_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    country = Column(String)
    market_cap = Column(BigInteger)
    currency = Column(String)
    exchange = Column(String)
    long_business_summary = Column(Text)
    full_time_employees = Column(Integer)
    raw_json = Column(JSON)   # full response from yfinance.get_info()


# --- Historical prices (history)
class StockPrice(Base):
    __tablename__ = "stock_price"

    symbol = Column(String, ForeignKey("ticker_info.symbol"), primary_key=True)
    date = Column(DateTime, index=True, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    dividends = Column(Float)
    stock_splits = Column(Float)


# --- Dividend history (get_dividends)
class Dividend(Base):
    __tablename__ = "dividend"

    symbol = Column(String, ForeignKey("ticker_info.symbol"), primary_key=True)
    date = Column(DateTime, index=True, primary_key=True)
    dividend = Column(Float)


# --- Stock split history (get_splits)
class StockSplit(Base):
    __tablename__ = "stock_split"

    symbol = Column(String, ForeignKey("ticker_info.symbol"), primary_key=True)
    date = Column(DateTime, index=True, primary_key=True)
    split_ratio = Column(Float)


# --- Corporate actions (get_actions → dividends + splits)
class CorporateAction(Base):
    __tablename__ = "corporate_action"

    symbol = Column(String, ForeignKey("ticker_info.symbol"), primary_key=True)
    date = Column(DateTime, index=True, primary_key=True)
    action_type = Column(String)   # "dividend" or "split"
    value = Column(Float)          # dividend amount or split ratio