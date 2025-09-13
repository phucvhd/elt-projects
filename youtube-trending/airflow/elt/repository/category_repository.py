import logging

from elt.config.config import Config
from elt.models.yt_base_models import VideoCategory
from elt.repository.repository import Repository

logger = logging.getLogger(__name__)

class CategoryRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_video_categories(self, video_categories: list[VideoCategory]) -> None:
        session = self.get_session()
        try:
            with session.begin():
                [session.merge(video_category) for video_category in video_categories]
            logger.info(f"✅ Data video_categories_lookup loaded successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to load video_categories_lookup data:", e)
            session.rollback()
            raise e
        finally:
            session.close()
