import requests
import time

class YoutubeApiClient:
    def __init__(self, api_key: str, region_code: str, max_results: int, base_url: str):
        self.api_key = api_key
        self.region_code = region_code
        self.max_results = max_results
        self.base_url = base_url

    def get_trending_videos(self, chart: str):
        params = {
            "part": "snippet,statistics",
            "chart": chart,
            "regionCode": self.region_code,
            "maxResults": self.max_results,
            "key": self.api_key
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            if response.status_code == 429:
                print("Rate limit hit, sleeping...")
                time.sleep(60)  # or longer depending on your quota window
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
