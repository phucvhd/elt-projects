import os
from dotenv import load_dotenv
from youtube_client import YoutubeApiClient

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
base_url = os.getenv("GOOGLE_DATA_V3_URL")
max_results = os.getenv("MAX_RESULT")
region_code = os.getenv("REGION_CODE")

# Init Youtube client
yt_client = YoutubeApiClient(api_key=api_key,
                             region_code=region_code,
                             max_results=max_results,
                             base_url=base_url)

# Extract data
responses = yt_client.get_trending_videos(chart="mostPopular")
if responses:
        for video in responses["items"]:
            title = video["snippet"]["title"]
            views = video["statistics"].get("viewCount", "N/A")
            print(f"{title} - {views} views")