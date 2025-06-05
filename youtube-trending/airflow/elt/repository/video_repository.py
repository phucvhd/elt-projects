import logging
from datetime import date

from sqlalchemy import Date, cast
from sqlalchemy.dialects.postgresql import insert

from elt.config.config import Config
from elt.repository.repository import Repository
from elt.models.yt_base_models import VideoStats, ChannelInfo, RawYoutubeTrending

logger = logging.getLogger(__name__)

class VideoRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_trending_videos(self, trending_videos_response) -> None:
        try:
            with self.session.begin():
                stmt = insert(RawYoutubeTrending).values(raw_json=trending_videos_response)
                self.session.execute(stmt)
            logger.info(f"✅ Data raw_youtube_trending loaded successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to load raw_youtube_trending data:", e)
            self.session.rollback()
            raise e

    def get_raw_trending_video(self, query_date: date) -> RawYoutubeTrending | None:
        try:
            with self.session.begin():
                raw_data = self.session.query(RawYoutubeTrending)\
                    .filter(cast(RawYoutubeTrending.fetch_timestamp, Date) == query_date)\
                    .order_by(RawYoutubeTrending.fetch_timestamp.desc())\
                    .first()
                if raw_data:
                    logger.info(f"Get raw data on {raw_data.fetch_timestamp} successfully")
                    self.session.close()
                else:
                    raise Exception(f"Raw data not found on date: {date}")
            return raw_data
        except Exception as e:
            logger.error("❌ Failed to get raw_youtube_trending data:", e)
            self.session.rollback()
            raise e

    def load_channel_info(self, channel_infos: list[ChannelInfo]) -> None:
        try:
            with self.session.begin():
                [self.session.merge(channel_info) for channel_info in channel_infos]
            logger.info(f"✅ Data channel_info loaded successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to load channel_info data:", e)
            self.session.rollback()
            raise e

    def load_video_stats(self, video_stats_list: list[VideoStats]) -> None:
            try:
                with self.session.begin():
                    [self.session.merge(video_stats) for video_stats in video_stats_list]
                logger.info(f"✅ Raw trending video transformed successfully into {self.dbname}")
            except Exception as e:
                logger.error("❌ Failed to transform video_stats data:", e)
                self.session.rollback()
                raise e
