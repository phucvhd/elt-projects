from service.category_service import CategoryService
from service.video_service import VideoService
from config.config import Config

# Load environment variables
config = Config()

# Init Extract service
video_service = VideoService(config)
category_service = CategoryService(config)

# Extract and Load trending videos
trending_videos_response = video_service.extract_trending_videos()
video_service.load_trending_videos(trending_videos_response)

# Extract and Load video_categories
video_categories_response = category_service.extract_video_categories()
category_service.load_video_categories(video_categories_response)

# Extract and Load channel infos
channel_info_response = video_service.extract_channel_infos(trending_videos_response)
video_service.load_channel_info(channel_info_response)