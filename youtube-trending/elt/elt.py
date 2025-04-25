import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from youtube_client import YoutubeApiClient
from sqlalchemy import create_engine, MetaData, Table, insert

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
base_url = os.getenv("GOOGLE_DATA_V3_URL")
max_results = os.getenv("MAX_RESULT")
region_code = os.getenv("REGION_CODE")
username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DB")

# Init Youtube client
yt_client = YoutubeApiClient(api_key=api_key,
                             region_code=region_code,
                             max_results=max_results,
                             base_url=base_url)

# Extract data
responses = yt_client.get_trending_videos(chart="mostPopular")
if responses:
        for video in responses["items"]:
            title = video["snippet"]["title"]
            views = video["statistics"].get("viewCount", "N/A")
            print(f"{title} - {views} views")

# Load data
try:
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}')
    metadata = MetaData()
    raw_youtube_trending_table = Table("raw_youtube_trending", metadata, autoload_with=engine)
    with engine.connect() as conn:
        stmt = insert(raw_youtube_trending_table).values(raw_json=responses)
        conn.execute(stmt)
        conn.commit()
    print(f"✅ Data loaded successfully into '{dbname}'")
except Exception as e:
    print("❌ Failed to load data:", e)
