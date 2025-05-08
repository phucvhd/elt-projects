from elt.client.youtube_client import YoutubeApiClient
from elt.config.config import Config
from elt.repository.video_repository import VideoRepository


def extract_channel_id(videos):
    channel_ids_list = []
    try:
        for channel_info in videos.get("items", []):
            channel_id = channel_info["snippet"]["channelId"]
            channel_ids_list.append(channel_id)
        return channel_ids_list
    except Exception as e:
        print("❌ Failed to load data:", e)


class VideoService:
    def __init__(self, config: Config):
        self.config = config
        self.yt_client = YoutubeApiClient(config)
        self.video_repository = VideoRepository(config)

    def extract_trending_videos(self):
        return self.yt_client.get_trending_videos(chart="mostPopular")

    def extract_channel_infos(self, trending_videos_response):
        channel_ids = extract_channel_id(trending_videos_response)
        return self.yt_client.get_channel_info(channel_ids)

    def load_trending_videos(self, trending_videos_response):
        print("Starting to load raw trending videos into database")
        self.video_repository.load_trending_videos(trending_videos_response)

    def load_channel_info(self, channel_info_response):
        print("Starting to load channel infos into database")
        self.video_repository.load_channel_info(channel_info_response)