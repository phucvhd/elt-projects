import logging

from elt.client.youtube_client import YoutubeApiClient
from elt.config.config import Config
from elt.helper.mapper import map_to_video_category
from elt.models.yt_base_models import VideoCategory
from elt.repository.category_repository import CategoryRepository

logger = logging.getLogger(__name__)

class CategoryService:
    def __init__(self, config: Config):
        self.config = config
        self.yt_client = YoutubeApiClient(config)
        self.category_repository = CategoryRepository(config)

    def extract_video_categories(self) -> dict | None:
        logger.info("Starting to extract video categories")
        try:
            return self.yt_client.get_video_categories()
        except Exception as e:
            logger.error("Failed to extract video categories", e)
            raise e

    def transform_to_video_categories(self, video_categories_response) -> list[VideoCategory]:
        logger.info("Starting to transform video categories response to video categories")
        try:
            return list([map_to_video_category(video_categories_item) for video_categories_item in video_categories_response.get("items", [])])
        except Exception as e:
            logger.error("Failed to transform video categories response to video categories", e)
            raise e

    def load_video_categories(self, video_categories: list[VideoCategory]) -> None:
        logger.info("Starting to load video categories into database")
        try:
            return self.category_repository.load_video_categories(video_categories)
        except Exception as e:
            logger.error("Failed to load video categories into database", e)
            raise e
