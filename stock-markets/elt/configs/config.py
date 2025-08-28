import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.USERNAME = os.getenv("POSTGRES_USER")
        self.PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.HOST = os.getenv("POSTGRES_HOST")
        self.PORT = os.getenv("POSTGRES_PORT")
        self.DBNAME = os.getenv("POSTGRES_DB")
        self.YFINANCE_PERIOD = os.getenv("YFINANCE_PERIOD")
        self.YFINANCE_INTERVAL = os.getenv("YFINANCE_INTERVAL")
