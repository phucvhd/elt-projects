import time
from datetime import date

from elt.models.yt_base_models import ChannelInfo, VideoCategory, VideoStats, ChannelStatistics


def map_to_channel_info(channel_info_item) -> ChannelInfo:
    return ChannelInfo(channel_id=channel_info_item["id"],
                       channel_title=channel_info_item["snippet"]["title"],
                       country=channel_info_item["snippet"].get("country", "undefined"),
                       published_at=channel_info_item["snippet"]["publishedAt"])

def map_to_video_category(video_categories_item) -> VideoCategory:
    return VideoCategory(category_name=video_categories_item["snippet"]["title"],
                         category_id=video_categories_item["id"])

def map_to_video_stats(trending_videos_item, trending_date: date) -> VideoStats:
    return VideoStats(video_id=trending_videos_item["id"],
                      title=trending_videos_item["snippet"]["title"],
                      description=trending_videos_item["snippet"]["description"],
                      category_id=trending_videos_item["snippet"]["categoryId"],
                      channel_id=trending_videos_item["snippet"]["channelId"],
                      published_at=trending_videos_item["snippet"]["publishedAt"],
                      trending_date=trending_date,
                      view_count=trending_videos_item["statistics"]["viewCount"] if 'viewCount' in trending_videos_item['statistics'] else 0,
                      like_count=trending_videos_item["statistics"]["likeCount"] if 'likeCount' in trending_videos_item['statistics'] else 0,
                      comment_count=trending_videos_item["statistics"]["commentCount"] if 'commentCount' in trending_videos_item['statistics'] else 0)

def map_to_channel_statistics(channel_statistics_item: dict) -> ChannelStatistics:
    return ChannelStatistics(channel_id=channel_statistics_item["id"],
                             view_count=channel_statistics_item["statistics"]["viewCount"] if 'viewCount' in channel_statistics_item["statistics"] else 0,
                             video_count=channel_statistics_item["statistics"]["videoCount"] if 'videoCount' in channel_statistics_item["statistics"] else 0,
                             subscriber_count=channel_statistics_item["statistics"]["subscriberCount"] if not channel_statistics_item["statistics"]["hiddenSubscriberCount"] else 0)
