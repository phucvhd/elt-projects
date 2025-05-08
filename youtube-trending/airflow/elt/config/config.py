import os

from dotenv import load_dotenv


class Config:
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    BSE_URL = os.getenv("GOOGLE_DATA_V3_URL")
    MAX_RESULTS = os.getenv("MAX_RESULT", 300)
    REGION_CODE = os.getenv("REGION_CODE")
    USERNAME = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")
    DBNAME = os.getenv("POSTGRES_DB")