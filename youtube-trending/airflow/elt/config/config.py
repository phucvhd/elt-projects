import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    def __init__(self, profile_env=None):
        profile = os.getenv("ENV_PROFILE", profile_env)
        dotenv_file = f".env.{profile}" if profile_env else ".env"
        load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / dotenv_file)
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        self.BSE_URL = os.getenv("GOOGLE_DATA_V3_URL")
        self.MAX_RESULTS = os.getenv("MAX_RESULT", 300)
        self.REGION_CODE = os.getenv("REGION_CODE")
        self.USERNAME = os.getenv("POSTGRES_USER")
        self.PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.HOST = os.getenv("POSTGRES_HOST")
        self.PORT = os.getenv("POSTGRES_PORT")
        self.DBNAME = os.getenv("POSTGRES_DB")
