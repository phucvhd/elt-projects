import logging

from elt.client.youtube_client import YoutubeApiClient
from elt.config.config import Config
from elt.helper.mapper import map_to_video_category
from elt.repository.category_repository import CategoryRepository

logger = logging.getLogger(__name__)

class CategoryService:
    def __init__(self, config: Config):
        self.config = config
        self.yt_client = YoutubeApiClient(config)
        self.category_repository = CategoryRepository(config)

    def extract_video_categories(self):
        logger.info("Starting to extract video categories")
        return self.yt_client.get_video_categories()

    def load_video_categories(self, video_categories_response):
        logger.info("Starting to load video categories into database")
        video_categories = list([map_to_video_category(video_categories_item) for video_categories_item in video_categories_response.get("item", [])])
        return self.category_repository.load_video_categories(video_categories)
