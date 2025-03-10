from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class InfluencerPlatform(BaseModel):
    __tablename__ = "influencer_platforms"

    influencer_id = Column(Integer, ForeignKey("influencers.id"), nullable=False)
    platform_name = Column(String(50), nullable=False)
    username = Column(String(100), nullable=False)
    profile_url = Column(String, nullable=False)
    followers = Column(Integer, default=0)
    posts = Column(Integer, default=0)
    engagement_rate = Column(Numeric(5, 2), default=0.00)

    # Relationships
    influencer = relationship("Influencer", back_populates="platforms") 