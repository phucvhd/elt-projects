from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert

from elt.config.config import Config
from elt.repository.repository import Repository


class VideoRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_trending_videos(self, trending_videos_response):
        try:
            engine = create_engine(self.POSTGRES_ENGINE_URL)
            metadata = MetaData()
            raw_youtube_trending_table = Table("raw_youtube_trending", metadata, autoload_with=engine)
            with engine.connect() as conn:
                stmt = insert(raw_youtube_trending_table).values(raw_json=trending_videos_response)
                conn.execute(stmt)
            print(f"✅ Data raw_youtube_trending loaded successfully into '{self.dbname}'")
        except Exception as e:
            print("❌ Failed to load raw_youtube_trending data:", e)

    def load_channel_info(self, channel_info_response):

        try:
            engine = create_engine(self.POSTGRES_ENGINE_URL)
            metadata = MetaData()
            channel_info_table = Table("channel_info", metadata, autoload_with=engine)
            with engine.connect() as conn:
                for item in channel_info_response.get("items", []):
                    stmt = insert(channel_info_table).values(channel_title=item["snippet"]["title"],
                                                             channel_id=item["id"],
                                                             country=item["snippet"].get("country", "undefined"),
                                                             published_at=item["snippet"]["publishedAt"])
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["channel_id"],
                        set_={"channel_title": item["snippet"]["title"],
                              "country": item["snippet"].get("country", "undefined"),
                              "published_at": item["snippet"]["publishedAt"]}
                    )
                    conn.execute(stmt)
            print(f"✅ Data channel_info loaded successfully into '{self.dbname}'")
        except Exception as e:
            print("❌ Failed to load channel_info data:", e)
