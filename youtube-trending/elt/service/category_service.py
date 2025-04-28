from client.youtube_client import YoutubeApiClient
from config.config import Config
from repository.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, config: Config):
        self.config = config
        self.yt_client = YoutubeApiClient(config)
        self.category_repository = CategoryRepository(config)

    def extract_video_categories(self):
        return self.yt_client.get_video_categories()

    def load_video_categories(self, video_categories_response):
        return self.category_repository.load_video_categories(video_categories_response)