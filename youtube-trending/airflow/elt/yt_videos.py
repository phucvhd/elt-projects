from elt.config.config import Config
from elt.service.category_service import CategoryService
from elt.service.video_service import VideoService

# Load environment variables
config = Config()

# Init Extract service
video_service = VideoService(config)
category_service = CategoryService(config)

# Extract and Load trending videos
def elt_trending_video():
    print("Starting elt_trending_video .....")
    try:
        trending_videos_response = video_service.extract_trending_videos()
        video_service.load_trending_videos(trending_videos_response)
        print("Ending elt_trending_video .....")
    except Exception as e:
        print(f"Error at elt_trending_video: ", e)


# Extract and Load video_categories
def elt_video_categories():
    print("Starting elt_video_categories .....")
    try:
        video_categories_response = category_service.extract_video_categories()
        category_service.load_video_categories(video_categories_response)
        print("Ending elt_video_categories .....")
    except Exception as e:
        print(f"Error at elt_video_categories: ", e)

# Extract and Load channel infos
def elt_channel_infos(trending_videos_response): # Should load from raw table
    channel_info_response = video_service.extract_channel_infos(trending_videos_response)
    video_service.load_channel_info(channel_info_response)