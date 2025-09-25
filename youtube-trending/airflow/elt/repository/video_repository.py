import logging
from datetime import date

from sqlalchemy import Date, cast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from elt.config.config import Config
from elt.repository.repository import Repository
from elt.models.yt_base_models import VideoStats, ChannelInfo, RawYoutubeTrending

logger = logging.getLogger(__name__)

class VideoRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_trending_videos(self, trending_videos_response) -> None:
        session = self.get_session()
        try:
            with session.begin():
                stmt = insert(RawYoutubeTrending).values(raw_json=trending_videos_response)
                session.execute(stmt)
            logger.info(f"✅ Data raw_youtube_trending loaded successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to load raw_youtube_trending data:", e)
            session.rollback()
            raise e
        finally:
            session.close()

    def get_raw_trending_video(self, query_date: date) -> RawYoutubeTrending | None:
        session = self.get_session()
        try:
            with session.begin():
                raw_data = session.query(RawYoutubeTrending)\
                    .filter(cast(RawYoutubeTrending.fetch_timestamp, Date) == query_date)\
                    .order_by(RawYoutubeTrending.fetch_timestamp.desc())\
                    .first()
                if raw_data:
                    logger.info(f"Get raw data on {raw_data.fetch_timestamp} successfully")
                    session.expunge(raw_data)
                else:
                    raise Exception(f"Raw data not found on date: {date}")
            return raw_data
        except Exception as e:
            logger.error("❌ Failed to get raw_youtube_trending data:", e)
            session.rollback()
            raise e
        finally:
            session.close()

    def load_video_stats(self, video_stats_list: list[VideoStats]) -> None:
        session = self.get_session()
        try:
            with session.begin():
                for video_stats in video_stats_list:
                    try:
                        with session.begin_nested():
                            session.merge(video_stats)
                    except IntegrityError as ie:
                        logger.warning(f"Skipping video_stats due to violation: {video_stats.channel_id}")
            logger.info(f"✅ Raw trending video transformed successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to transform video_stats data:", e)
            session.rollback()
            raise e
        finally:
            session.close()
