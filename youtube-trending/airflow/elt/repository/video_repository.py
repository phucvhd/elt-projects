from sqlalchemy.dialects.postgresql import insert

from elt.config.config import Config
from elt.repository.repository import Repository
from elt.models.yt_base_models import VideoStats, ChannelInfo, RawYoutubeTrending


class VideoRepository(Repository):
    def __init__(self, config: Config):
        super().__init__(config)

    def load_trending_videos(self, trending_videos_response):
        try:
            with self.session.begin():
                stmt = insert(RawYoutubeTrending).values(raw_json=trending_videos_response)
                self.session.execute(stmt)
            print(f"✅ Data raw_youtube_trending loaded successfully into '{self.dbname}'")
        except Exception as e:
            print("❌ Failed to load raw_youtube_trending data:", e)
            self.session.rollback()
            raise e

    def load_channel_info(self, channel_info_response):
        try:
            with self.session.begin():
                for item in channel_info_response.get("items", []):
                    stmt = insert(ChannelInfo).values(channel_title=item["snippet"]["title"],
                                                             channel_id=item["id"],
                                                             country=item["snippet"].get("country", "undefined"),
                                                             published_at=item["snippet"]["publishedAt"])
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["channel_id"],
                        set_={"channel_title": item["snippet"]["title"],
                              "country": item["snippet"].get("country", "undefined"),
                              "published_at": item["snippet"]["publishedAt"]}
                    )

                    self.session.execute(stmt)
            print(f"✅ Data channel_info loaded successfully into '{self.dbname}'")
        except Exception as e:
            print("❌ Failed to load channel_info data:", e)
            self.session.rollback()
            raise e

    def transform_video_stats(self, trending_videos_response):
            try:
                with self.session.begin():
                    for item in trending_videos_response.get("items", []):
                        video_stat = {'video_id': item["id"],
                                        'title': item["snippet"]["title"],
                                        'description': item['snippet']['description'],
                                        'category_id': item['snippet']['categoryId'],
                                        'channel_id': item['snippet']['channelId'],
                                        'published_at': item['snippet']['publishedAt'],
                                        'view_count': item['statistics']['viewCount'] if 'viewCount' in item['statistics'] else 0,
                                        'like_count': item['statistics']['likeCount'] if 'likeCount' in item['statistics'] else 0,
                                        'comment_count': item['statistics']['commentCount'] if 'commentCount' in item['statistics'] else 0
                        }
                        stmt = insert(VideoStats).values(**video_stat)

                        update_columns = {
                            col.name: stmt.excluded[col.name]
                            for col in VideoStats.__table__.columns
                            if col.name != 'video_id'  # don't update primary key
                        }

                        stmt = stmt.on_conflict_do_update(
                            index_elements=['video_id'],  # column(s) to check conflict on
                            set_=update_columns
                        )

                        self.session.execute(stmt)
                print(f"✅ Raw trending video transformed successfully into video_stats in '{self.dbname}'")
            except Exception as e:
                print("❌ Failed to transform video_stats data:", e)
                self.session.rollback()
                raise e
