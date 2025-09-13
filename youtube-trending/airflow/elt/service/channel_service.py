import logging

from elt.client.youtube_client import YoutubeApiClient
from elt.config.config import Config
from elt.helper.mapper import map_to_channel_info, map_to_channel_statistics
from elt.models.yt_base_models import RawYoutubeTrending, ChannelInfo, ChannelStatistics
from elt.repository.channel_repository import ChannelRepository

logger = logging.getLogger(__name__)

class ChannelService:
    def __init__(self, config: Config):
        self.config = config
        self.yt_client = YoutubeApiClient(config)
        self.channel_repository = ChannelRepository(config)

    def extract_channel_id(self, raw_video_data: RawYoutubeTrending) -> list | None:
        channel_ids_list = []
        try:
            for channel_info in raw_video_data.raw_json.get("items", []):
                channel_id = channel_info["snippet"]["channelId"]
                channel_ids_list.append(channel_id)
            return channel_ids_list
        except Exception as e:
            logger.error("❌ Error when extracting channel id from raw data", e)
            raise e

    def extract_channel_infos(self, raw_video_data: RawYoutubeTrending) -> dict | None:
        logger.info("Extracting channel infos")
        channel_ids = self.extract_channel_id(raw_video_data)
        return self.yt_client.fetch_channel_infos(channel_ids)

    def extract_channel_infos_from_ids(self, channel_ids: []) -> dict | None:
        logger.info("Extracting channel infos from provided channel ids")
        try:
            return self.yt_client.fetch_channel_infos(channel_ids)
        except Exception as e:
            logger.error("Error when extracting channel infos from provided channel ids", e)
            exit(1)

    def extract_channel_statistics(self, channel_ids: []) -> dict | None:
        logger.info("Extracting channel statistics")
        try:
            return self.yt_client.fetch_channel_statistics(channel_ids)
        except Exception as e:
            logger.error("Error when extracting channel statistics", e)
            exit(1)

    def transform_to_channel_infos(self, channel_info_response: dict) -> list[ChannelInfo]:
        logger.info("Starting to transform channel info response to channel info")
        try:
            return list([map_to_channel_info(channel_info_item) for channel_info_item in
                         channel_info_response.get("items", [])])
        except Exception as e:
            logger.error("Error when transform channel info response to channel info", e)
            raise e

    def transform_to_channel_statistics(self, channel_statistics_response: dict) -> list[ChannelStatistics]:
        logger.info("Starting to transform channel statistics response to channel statistics")
        try:
            return list([map_to_channel_statistics(channel_statistics_item) for channel_statistics_item in
                         channel_statistics_response.get("items", [])])
        except Exception as e:
            logger.error("Error when transform channel info response to channel info", e)
            exit(1)

    def load_channel_info(self, channel_infos: list[ChannelInfo]) -> None:
        logger.info("Starting to load channel infos into database")
        try:
            return self.channel_repository.load_channel_info(channel_infos)
        except Exception as e:
            logger.error("Error when loading channel infos into database", e)
            raise e

    def load_channel_statistics(self, channel_statistics: list[ChannelStatistics]) -> None:
        logger.info("Starting to load channel statistics into database")
        try:
            return self.channel_repository.load_channel_statistics(channel_statistics)
        except Exception as e:
            logger.error("Error when loading channel statistics into database", e)
            exit(1)

    def check_channel_infos_is_existed(self, channel_ids: list) -> tuple:
        logger.info("Starting to get channel info by provided ids")
        ids_not_exits = []
        try:
            channel_infos = self.channel_repository.get_channel_info_by_ids(channel_ids)
            for channel_id in channel_ids:
                if channel_id not in channel_infos:
                    ids_not_exits.append(channel_id)
                    channel_ids.remove(channel_id)
            logger.info(f"There are {len(ids_not_exits)} ids are not exits, {len(channel_ids)} ids are exited in db")
            return channel_ids, ids_not_exits
        except Exception as e:
            logger.error("Error when loading channel infos into database", e)
            raise e