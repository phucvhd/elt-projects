import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.base_url = os.getenv("GOOGLE_DATA_V3_URL")
        self.max_results = os.getenv("MAX_RESULT", 300)
        self.region_code = os.getenv("REGION_CODE")
        self.username = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.dbname = os.getenv("POSTGRES_DB")