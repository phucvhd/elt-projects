import logging

from elt.client.youtube_client import YoutubeApiClient
from elt.config.config import Config
from elt.helper.mapper import map_to_channel_info, map_to_video_stats
from elt.repository.video_repository import VideoRepository


def extract_channel_id(videos) -> list | None:
    channel_ids_list = []
    try:
        for channel_info in videos.get("items", []):
            channel_id = channel_info["snippet"]["channelId"]
            channel_ids_list.append(channel_id)
        return channel_ids_list
    except Exception as e:
        logger.info("❌ Failed to load data:", e)
        raise e

logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self, config: Config):
        self.config = config
        self.yt_client = YoutubeApiClient(config)
        self.video_repository = VideoRepository(config)

    def extract_trending_videos(self) -> None:
        logger.info("Extracting trending videos")
        return self.yt_client.get_trending_videos(chart="mostPopular")

    def extract_channel_infos(self, trending_videos_response) -> dict | None:
        logger.info("Extracting channel infos")
        channel_ids = extract_channel_id(trending_videos_response)
        return self.yt_client.get_channel_info(channel_ids)

    def load_trending_videos(self, trending_videos_response) -> None:
        logger.info("Starting to load raw trending videos into database")
        self.video_repository.load_trending_videos(trending_videos_response)

    def load_channel_info(self, channel_info_response) -> None:
        logger.info("Starting to load channel infos into database")
        channel_infos = list([map_to_channel_info(channel_info_item) for channel_info_item in channel_info_response.get("items", [])])
        self.video_repository.load_channel_info(channel_infos)

    def transform_video_stats(self, trending_videos_response) -> None:
        logger.info("Starting to transform trending_videos_response to video stats")
        video_stats_list = list([map_to_video_stats(trending_videos_item) for trending_videos_item in trending_videos_response.get("items", [])])
        self.video_repository.load_video_stats(video_stats_list)
