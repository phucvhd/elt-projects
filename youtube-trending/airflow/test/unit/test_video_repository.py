from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from elt.config.config import Config
from elt.models.yt_base_models import Base, ChannelInfo, VideoStats
from elt.repository.video_repository import VideoRepository

config = Config("test")

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_load_trending_videos_pass(caplog, session):
    with caplog.at_level("INFO"):
        repo = VideoRepository(config)
        repo.session = session
        trending_videos_response = {
            "raw_json": "mock_json"
        }
        repo.load_trending_videos(trending_videos_response)

    assert "✅ Data raw_youtube_trending loaded successfully into youtube_trending_test_db" == caplog.records[0].message

def test_load_channel_info_pass(caplog, session):
    with caplog.at_level("INFO"):
        repo = VideoRepository(config)
        repo.session = session
        channel_info_1 = ChannelInfo(
            channel_id="mock_id_1",
            channel_title="mock_title_1",
            country="country",
            published_at=datetime.now()
        )
        channel_info_2 = ChannelInfo(
            channel_id="mock_id_2",
            channel_title="mock_title_2",
            country="country",
            published_at=datetime.now()
        )
        channel_infos = list([channel_info_1, channel_info_2])
        repo.load_channel_info(channel_infos)

    assert "✅ Data channel_info loaded successfully into youtube_trending_test_db" == caplog.records[0].message

def test_load_video_stats_pass(caplog, session):
    with caplog.at_level("INFO"):
        repo = VideoRepository(config)
        repo.session = session
        video_stats_1 = VideoStats(video_id="mock_id_1",
                      title="mock_title_1",
                      description="mock_description",
                      category_id="mock_category_id",
                      channel_id="mock_channel_id",
                      published_at=datetime.now(),
                      view_count=0,
                      like_count=0,
                      comment_count=0)
        video_stats_2 = VideoStats(video_id="mock_id_2",
                      title="mock_title_2",
                      description="mock_description",
                      category_id="mock_category_id",
                      channel_id="mock_channel_id",
                      published_at=datetime.now(),
                      view_count=0,
                      like_count=0,
                      comment_count=0)
        video_stats_list = list([video_stats_1, video_stats_2])
        repo.load_video_stats(video_stats_list)

    assert "✅ Raw trending video transformed successfully into youtube_trending_test_db" == caplog.records[0].message

if __name__ == "__main__":
    pytest.main(["-v", "test_video_repository.py"])
