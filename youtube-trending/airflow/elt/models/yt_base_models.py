from sqlalchemy import Column, Integer, JSON, TIMESTAMP, func, Text, String, Date, ForeignKey, text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class RawYoutubeTrending(Base):
    __tablename__ = 'raw_youtube_trending'
    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_json = Column(JSON, nullable=False)
    fetch_timestamp = Column(TIMESTAMP, server_default=func.now())

class VideoCategory(Base):
    __tablename__ = 'video_categories'
    category_id = Column(String, primary_key=True)
    category_name = Column(Text, nullable=False)

class ChannelInfo(Base):
    __tablename__ = 'channel_infos'
    channel_id = Column(String, primary_key=True)
    channel_title = Column(Text, nullable=False)
    country = Column(Text, nullable=False)
    published_at = Column(TIMESTAMP, nullable=False)

class VideoStats(Base):
    __tablename__ = 'video_stats'
    video_id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(String, ForeignKey('video_categories.category_id'), nullable=False)
    channel_id = Column(String, ForeignKey('channel_infos.channel_id'), nullable=False)
    published_at = Column(TIMESTAMP, nullable=False)
    trending_date = Column(Date, primary_key=True, nullable=False, server_default=text('CURRENT_DATE'))
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    channel_infos = relationship("ChannelInfo")
    video_categories = relationship("VideoCategory")

class ChannelStatistics(Base):
    __tablename__ = 'channel_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String, ForeignKey('channel_infos.channel_id'), nullable=False)
    fetch_timestamp = Column(TIMESTAMP, server_default=func.now())
    view_count = Column(BigInteger)
    video_count = Column(BigInteger)
    subscriber_count = Column(BigInteger, nullable=True)
    channel_infos = relationship("ChannelInfo")