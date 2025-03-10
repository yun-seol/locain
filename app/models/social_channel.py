from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class SocialPlatform(str, enum.Enum):
    KAKAO = "kakao"
    NAVER = "naver"
    GOOGLE = "google"
    APPLE = "apple"

class SocialChannel(Base):
    __tablename__ = "social_channels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(SQLEnum(SocialPlatform))
    channel_name = Column(String)
    channel_url = Column(String)
    followers_count = Column(Integer, default=0)
    average_views = Column(Integer, default=0)
    average_likes = Column(Integer, default=0)
    average_comments = Column(Integer, default=0)
    average_shares = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    followers = Column(Integer, default=0)
    posts = Column(Integer, default=0)
    last_sync_at = Column(DateTime, nullable=True)
    platform_specific_data = Column(String, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="social_channels")
    blog_post_rankings = relationship("BlogPostRanking", back_populates="channel")

class BlogPostRanking(Base):
    __tablename__ = "blog_post_rankings"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("social_channels.id"))
    post_url = Column(String)
    title = Column(String)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    ranking_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    channel = relationship("SocialChannel", back_populates="blog_post_rankings") 