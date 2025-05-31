from requests import session
from sqlalchemy.dialects.postgresql import insert

from elt.config.config import Config
from elt.models.yt_base_models import VideoCategory
from elt.repository.repository import Repository


class CategoryRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_video_categories(self, video_categories_response):
        try:
            with self.session.begin():
                for item in video_categories_response.get("items", []):
                    stmt = insert(VideoCategory).values(category_name=item["snippet"]["title"],
                                                                        category_id=item["id"])
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["category_id"],
                        set_={"category_name": item["snippet"]["title"]}
                    )
                    self.session.execute(stmt)
            print(f"✅ Data video_categories_lookup loaded successfully into '{self.dbname}'")
        except Exception as e:
            print("❌ Failed to load video_categories_lookup data:", e)
            self.session.rollback()
            raise e
