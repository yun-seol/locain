from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class ChannelAnalytics(BaseModel):
    __tablename__ = "channel_analytics"

    channel_id = Column(Integer, ForeignKey("social_channels.id"))
    date = Column(DateTime)
    followers_count = Column(Integer)
    posts_count = Column(Integer)
    total_views = Column(Integer)
    total_likes = Column(Integer)
    total_comments = Column(Integer)
    total_shares = Column(Integer)

    # Relationships
    channel = relationship("SocialChannel", back_populates="channel_analytics") 