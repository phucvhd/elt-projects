import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from elt.config.config import Config
from elt.models.yt_base_models import Base, VideoCategory
from elt.repository.category_repository import CategoryRepository

config = Config("test")

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_load_video_categories(caplog, session):
    with caplog.at_level("INFO"):
        repo = CategoryRepository(config)
        repo.session = session
        video_category_1 = VideoCategory(
            category_id="mock_id_1",
            category_name="mock_category_1"
        )
        video_category_2 = VideoCategory(
            category_id="mock_id_2",
            category_name="mock_category_2"
        )
        video_categories = list([video_category_1, video_category_2])
        repo.load_video_categories(video_categories)

    assert "✅ Data video_categories_lookup loaded successfully into youtube_trending_test_db" == caplog.records[0].message

if __name__ == "__main__":
    pytest.main(["-v", "test_category_repository.py"])
