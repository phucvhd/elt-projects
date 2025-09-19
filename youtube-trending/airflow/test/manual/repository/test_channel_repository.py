import logging

from elt.config.config import Config
from elt.repository.channel_repository import ChannelRepository

logger = logging.getLogger(__name__)

config = Config(profile_env="test")
channel_repository = ChannelRepository(config)

def test_check_table_exits():
    is_exits = channel_repository.check_table_exits("top_channels")
    assert is_exits is True

def test_get_top_channel_ids():
    result = channel_repository.get_top_channel_ids()
    assert len(result) > 0