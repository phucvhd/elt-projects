import logging

from elt.config.config import Config
from elt.service.channel_service import ChannelService

config = Config(profile_env="dev")
channel_service = ChannelService(config)

logger = logging.getLogger(__name__)

def test_extract_channel_statistics():
    response = channel_service.extract_channel_statistics(["UCBVrn_SGKAOv3yKPi4Oc3-A"])
    statistics = channel_service.transform_to_channel_statistics(response)
    channel_service.load_channel_statistics(statistics)

def test_extract_channel_info_from_ids():
    channel_ids = ["UCBVrn_SGKAOv3yKPi4Oc3-A"]
    try:
        # check if ids exits
        checked_ids = channel_service.check_channel_infos_is_existed(channel_ids)
        if len(checked_ids[1]) > 0:
            logger.info(f"Extracting {len(checked_ids[1])} channel info(s) not in db")
            channel_info_response = channel_service.extract_channel_infos_from_ids(checked_ids[1])
            channel_infos = channel_service.transform_to_channel_infos(channel_info_response)
            channel_service.load_channel_info(channel_infos)
        else:
            logger.info(f"Channel info(s) exited, skip extract_channel_info_from_ids")
    except Exception as e:
        logger.error(f"Error at extract_channel_info_from_ids: ", e)
        exit(1)

