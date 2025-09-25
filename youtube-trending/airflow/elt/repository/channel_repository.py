import logging

from sqlalchemy import inspect, Table, MetaData

from elt.config.config import Config
from elt.models.yt_base_models import ChannelInfo, ChannelStatistics
from elt.repository.repository import Repository

logger = logging.getLogger(__name__)

class ChannelRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_channel_info(self, channel_infos: list[ChannelInfo]) -> None:
        session = self.get_session()
        try:
            with session.begin():
                [session.merge(channel_info) for channel_info in channel_infos]
            logger.info(f"✅ {len(channel_infos)} channel_infos loaded successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to load channel_infos", e)
            session.rollback()
            raise e
        finally:
            session.close()

    def load_channel_statistics(self, channel_statistics: list[ChannelStatistics]) -> None:
        session = self.get_session()
        try:
            with session.begin():
                [session.merge(channel_statistic) for channel_statistic in channel_statistics]
            logger.info(f"✅ Data from channel_statistics loaded successfully into {self.dbname}")
        except Exception as e:
            logger.error("❌ Failed to load channel_statistics", e)
            session.rollback()
            raise e
        finally:
            session.close()

    def get_channel_info_by_ids(self, ids: []) -> list[str] | None:
        session = self.get_session()
        try:
            with session.begin():
                rows = session.query(ChannelInfo.channel_id).filter(ChannelInfo.channel_id.in_(ids)).all()
            return [row.channel_id for row in rows]
        except Exception as e:
            logger.error("❌ Failed to get channel info by ids", e)
            session.rollback()
            raise e
        finally:
            session.close()

    def get_top_channel_ids(self) -> list[str] | None:
        session = self.get_session()
        try:
            if self.check_table_exits("top_channels"):
                logger.info("Table top_channels exits. Receiving channel ids")
                top_channels_table = Table("top_channels", MetaData(), autoload_with=self.engine)
                with session.begin():
                    rows = session.query(top_channels_table).all()
                return [row.channel_id for row in rows]
            raise Exception("Table top_channels does not exit")
        except Exception as e:
            logger.error("❌ Failed to get top channel info", e)
            session.rollback()
            raise e
        finally:
            session.close()

    def check_table_exits(self, table_name: str) -> bool:
        try:
            inspector = inspect(self.engine)
            return inspector.has_table(table_name)
        except Exception as e:
            logger.error("❌ Failed to check table existence", e)
            raise e