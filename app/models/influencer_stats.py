from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class InfluencerStats(BaseModel):
    __tablename__ = "influencer_stats"

    influencer_id = Column(Integer, ForeignKey("influencers.id"), unique=True, nullable=False)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)
    average_likes = Column(Integer, default=0)
    average_comments = Column(Integer, default=0)
    engagement_rate = Column(Numeric(5, 2), default=0.00)

    # Relationships
    influencer = relationship("Influencer", back_populates="stats") 