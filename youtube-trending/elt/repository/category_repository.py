from config.config import Config
from repository.repository import Repository
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

class CategoryRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_video_categories(self, video_categories_response):
        try:
            engine = create_engine(self.POSTGRES_ENGINE_URL)
            metadata = MetaData()
            video_categories_lookup_table = Table("video_categories_lookup", metadata, autoload_with=engine)
            with engine.connect() as conn:
                for item in video_categories_response.get("items", []):
                    stmt = insert(video_categories_lookup_table).values(category_name=item["snippet"]["title"],
                                                                        category_id=item["id"])
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["category_id"],
                        set_={"category_name": item["snippet"]["title"]}
                    )
                    conn.execute(stmt)
                conn.commit()
            print(f"✅ Data video_categories_lookup loaded successfully into '{self.dbname}'")
        except Exception as e:
            print("❌ Failed to load video_categories_lookup data:", e)
