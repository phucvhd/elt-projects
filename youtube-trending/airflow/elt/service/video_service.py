import logging
from datetime import date, datetime

from elt.client.aws_client import AwsClient
from elt.client.youtube_client import YoutubeApiClient
from elt.config.config import Config
from elt.helper.mapper import map_to_channel_info, map_to_video_stats
from elt.models.yt_base_models import RawYoutubeTrending, VideoStats, ChannelInfo
from elt.repository.video_repository import VideoRepository


def extract_channel_id(raw_video: RawYoutubeTrending) -> list | None:
    channel_ids_list = []
    try:
        for channel_info in raw_video.raw_json.get("items", []):
            channel_id = channel_info["snippet"]["channelId"]
            channel_ids_list.append(channel_id)
        return channel_ids_list
    except Exception as e:
        logger.info("❌ Failed to load data:", e)
        raise e

logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self, config: Config):
        self.yt_client = YoutubeApiClient(config)
        self.video_repository = VideoRepository(config)
        self.aws_client = AwsClient(config)

    def extract_trending_videos(self) -> dict | None:
        logger.info("Extracting trending videos")
        return self.yt_client.fetch_trending_videos(chart="mostPopular")

    def extract_channel_infos(self, raw_video_data: RawYoutubeTrending) -> dict | None:
        logger.info("Extracting channel infos")
        channel_ids = extract_channel_id(raw_video_data)
        return self.yt_client.fetch_channel_infos(channel_ids)

    def transform_to_video_stats(self, raw_video_data: RawYoutubeTrending) -> list[VideoStats]:
        logger.info("Starting to transform raw trending videos to video stats")
        try:
            return list([map_to_video_stats(trending_videos_item, raw_video_data.fetch_timestamp.date()) for
                         trending_videos_item in raw_video_data.raw_json.get("items", [])])
        except Exception as e:
            logger.error("Error when transform raw trending videos to video stats")
            raise e

    def transform_to_video_stats_v2(self, raw_video_data: dict, trending_date: date) -> list[VideoStats]:
        logger.info("Starting to transform raw trending videos to video stats")
        try:
            return list([map_to_video_stats(trending_videos_item, trending_date) for
                         trending_videos_item in raw_video_data.get("items", [])])
        except Exception as e:
            logger.error("Error when transform raw trending videos to video stats")
            raise e

    def load_trending_videos(self, trending_videos_response: dict) -> None:
        logger.info("Starting to load raw trending videos into database")
        try:
            return self.video_repository.load_trending_videos(trending_videos_response)
        except Exception as e:
            logger.error("Error when loading raw trending videos into database")
            raise e

    def load_trending_videos_to_bucket(self, trending_videos_response: dict) -> None:
        logger.info(f"Starting to load raw trending videos into bucket {self.aws_client.AWS_BUCKET_NAME}")
        try:
            return self.aws_client.upload_raw_data(trending_videos_response)
        except Exception as e:
            logger.error(f"Error when loading raw trending videos into bucket {self.aws_client.AWS_BUCKET_NAME}", e)
            raise e

    def load_video_stats(self, video_stats: list[VideoStats]) -> None:
        logger.info("Starting to load video stats into database")
        try:
            return self.video_repository.load_video_stats(video_stats)
        except Exception as e:
            logger.error("Error when loading video stats into database")
            raise e

    def get_raw_trending_video(self, query_date: date) -> RawYoutubeTrending | None:
        logger.info(f"Starting to get raw_trending_video on {query_date}")
        try:
            return self.video_repository.get_raw_trending_video(query_date)
        except Exception as e:
            logger.error("Error when getting raw_trending_video from database", e)
            raise e

    def get_raw_trending_video_from_bucket(self, query_date: date) -> dict | None:
        logger.info(f"Starting to get raw_trending_video from bucket {self.aws_client.AWS_BUCKET_NAME} on {query_date}")
        try:
            today_str = query_date.strftime('%Y%m%d')
            responses = self.aws_client.get_object_keys_with_pattern(pattern=today_str)
            if not responses:
                raise Exception(f"No key found on {query_date}")
            return self.aws_client.get_json_as_dict(responses[0])
        except Exception as e:
            logger.error("Error when getting raw_trending_video from database", e)
            raise e
