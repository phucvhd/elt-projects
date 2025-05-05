import requests
import time

from elt.config.config import Config


class YoutubeApiClient:
    def __init__(self, config: Config):
        self.api_key = config.API_KEY
        self.region_code = config.REGION_CODE
        self.max_results = config.MAX_RESULTS
        self.base_url = config.BSE_URL

    def get_trending_videos(self, chart: str):
        params = {
            "part": "snippet,statistics",
            "chart": chart,
            "regionCode": self.region_code,
            "maxResults": self.max_results,
            "key": self.api_key
        }

        response = requests.get(self.base_url + "videos", params=params)

        if response.status_code == 200:
            return response.json()
        else:
            if response.status_code == 429:
                print("Rate limit hit, sleeping...")
                time.sleep(60)  # or longer depending on your quota window
            print(f"Error from get_trending_videos: {response.status_code}")
            print(response.text)
            return None

    def get_video_categories(self):
        params = {
            "part": "snippet",
            "regionCode": self.region_code,
            "key": self.api_key
        }
        response = requests.get(self.base_url + "videoCategories", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            if response.status_code == 429:
                print("Rate limit hit, sleeping...")
                time.sleep(60)  # or longer depending on your quota window
            print(f"Error from get_video_categories: {response.status_code}")
            print(response.text)
            return None

    def get_channel_info(self, channel_ids: []):
        params = {
            "part": "snippet",
            "id": channel_ids,
            "key": self.api_key
        }
        response = requests.get(self.base_url + "channels", params=params)

        if response.status_code == 200:
            return response.json()
        else:
            if response.status_code == 429:
                print("Rate limit hit, sleeping...")
                time.sleep(60)  # or longer depending on your quota window
            print(f"Error from get_channel_info: {response.status_code}")
            print(response.text)
            return None