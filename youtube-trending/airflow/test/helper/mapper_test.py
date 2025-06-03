import logging
from datetime import datetime

import pytest

from elt.helper.mapper import map_to_channel_info, map_to_video_category, map_to_video_stats
from elt.models.yt_base_models import ChannelInfo, VideoCategory, VideoStats

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.mark.parametrize("mock_id, mock_title, mock_country, mock_published_at",
                         [("mock_id", "mock_title", "mock_country", datetime.now())],
                         ids=["Positive"])
def test_map_to_channel_info_pass(mock_id, mock_title, mock_country, mock_published_at):
    channel_info_response = {
                "id": mock_id,
                "snippet": {
                    "title": mock_title,
                    "country": mock_country,
                    "publishedAt": mock_published_at
                }
            }
    channel_info = ChannelInfo(channel_id=mock_id,
                channel_title=mock_title,
                country=mock_country,
                published_at=mock_published_at)
    result = map_to_channel_info(channel_info_response)

    assert result
    assert channel_info.channel_id == result.channel_id, "channel id should the same"
    assert channel_info.channel_title == result.channel_title, "channel title should the same"
    assert channel_info.country == result.country, "channel country should the same"
    assert channel_info.published_at == result.published_at, "channel published date should the same"
    logger.info("✅ Test case map_to_channel_info_pass: Passed!")

def test_map_to_video_category_pass():
    video_categories_item = {
        "id": "test",
        "snippet": {
            "title": "title"
        }
    }
    video_categories = VideoCategory(category_name="title",
                  category_id="test")
    result = map_to_video_category(video_categories_item)

    assert result
    assert video_categories.category_id == result.category_id
    assert video_categories.category_name == result.category_name
    logger.info("✅ Test case map_to_video_category_pass: Passed!")

def test_map_to_video_stats_pass():
    trending_videos_item = {
        "id": "mock_id",
        "snippet": {
            "title": "mock_title",
            "description": "mock_description",
            "categoryId": "mock_category_id",
            "channelId": "mock_channel_id",
            "publishedAt": datetime.now()
        },
        "statistics": {
            "viewCount": 0,
            "likeCount": 0,
            "commentCount": 0
        }
    }
    video_stats = VideoStats(video_id="mock_id",
                      title="mock_title",
                      description="mock_description",
                      category_id="mock_category_id",
                      channel_id="mock_channel_id",
                      published_at=trending_videos_item["snippet"]["publishedAt"],
                      view_count=0,
                      like_count=0,
                      comment_count=0)
    result = map_to_video_stats(trending_videos_item)
    assert result
    assert video_stats.video_id == result.video_id
    assert video_stats.title == result.title
    assert video_stats.description == result.description
    assert video_stats.category_id == result.category_id
    assert video_stats.channel_id == result.channel_id
    assert video_stats.view_count == result.view_count
    assert video_stats.like_count == result.like_count
    assert video_stats.comment_count == result.comment_count

if __name__ == "__main__":
    pytest.main(["-v", "mapper_test.py"])
