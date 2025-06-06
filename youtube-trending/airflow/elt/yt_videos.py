import logging
from datetime import date

from elt.config.config import Config
from elt.service.category_service import CategoryService
from elt.service.video_service import VideoService

# Load environment variables
config = Config()

# Init Extract service
video_service = VideoService(config)
category_service = CategoryService(config)

logger = logging.getLogger(__name__)

# Extract and Load trending videos
def extract_raw_trending_video():
    logger.info("Starting extract_raw_trending_video .....")
    try:
        trending_videos_response = video_service.extract_trending_videos()
        video_service.load_trending_videos(trending_videos_response)
        logger.info("Ending extract_raw_trending_video .....")
    except Exception as e:
        logger.error(f"Error at extract_raw_trending_video: ", e)
        exit(1)

def extract_channel_info(query_date: date):
    logger.info(f"Starting extract_channel_info on date: {date} .....")
    try:
        # load_raw_video by date
        raw_trending_video = video_service.get_raw_trending_video(query_date)

        channel_info_response = video_service.extract_channel_infos(raw_trending_video)
        video_service.load_channel_info(channel_info_response)
        logger.info("Ending extract_channel_info .....")
    except Exception as e:
        logger.error(f"Error at extract_channel_info: ", e)
        exit(1)

def transform_video_stats(query_date: date):
    logger.info(f"Starting transform_video_stats on date: {query_date} .....")
    try:
        # load_raw_video by date
        raw_trending_video = video_service.get_raw_trending_video(query_date)

        video_service.transform_video_stats(raw_trending_video)
        logger.info("Ending transform_video_stats .....")
    except Exception as e:
        logger.error(f"Error at transform_video_stats: ", e)
        exit(1)

# Extract and Load video_categories
def extract_video_categories():
    logger.info("Starting extract_video_categories .....")
    try:
        logger.info("Extracting video_categories .....")
        video_categories_response = category_service.extract_video_categories()
        logger.info("Loading video_categories .....")
        category_service.load_video_categories(video_categories_response)
        logger.info("Ending extract_video_categories .....")
    except Exception as e:
        logger.error(f"Error at extract_video_categories: ", e)
        exit(1)
