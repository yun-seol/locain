from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Date
from sqlalchemy.orm import relationship
from .base import BaseModel

class BlogPostRanking(BaseModel):
    __tablename__ = "blog_post_rankings"

    channel_id = Column(Integer, ForeignKey("social_channels.channel_id"), nullable=False)
    post_url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    ranking_date = Column(Date, nullable=False)

    # Relationships
    channel = relationship("SocialChannel", back_populates="blog_post_rankings") 