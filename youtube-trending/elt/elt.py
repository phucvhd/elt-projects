import os
from dotenv import load_dotenv

from youtube_client import YoutubeApiClient
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

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
trending_videos_response = yt_client.get_trending_videos(chart="mostPopular")
video_categories_response = yt_client.get_video_categories()

# Load data
try:
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}')
    metadata = MetaData()
    raw_youtube_trending_table = Table("raw_youtube_trending", metadata, autoload_with=engine)
    with engine.connect() as conn:
        stmt = insert(raw_youtube_trending_table).values(raw_json=trending_videos_response)
        conn.execute(stmt)
        conn.commit()
    print(f"✅ Data raw_youtube_trending loaded successfully into '{dbname}'")
except Exception as e:
    print("❌ Failed to load data:", e)

# Load video_categories
try:
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}')
    # if engine.dialect.has_table(engine.connect(), "video_categories_lookup"):
    #     print("Table exists!")
    metadata = MetaData()
    video_categories_lookup_table = Table("video_categories_lookup", metadata, autoload_with=engine)
    with engine.connect() as conn:
        for item in video_categories_response.get("items", []):
            stmt = insert(video_categories_lookup_table).values(category_name=item["snippet"]["title"], category_id=item["id"])
            stmt = stmt.on_conflict_do_update(
                index_elements=["category_id"],
                set_={"category_name": item["snippet"]["title"]}
            )
            conn.execute(stmt)
        conn.commit()
    print(f"✅ Data video_categories_lookup loaded successfully into '{dbname}'")
except Exception as e:
    print("❌ Failed to load data:", e)