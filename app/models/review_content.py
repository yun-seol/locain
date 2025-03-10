from sqlalchemy import Column, String, Enum, Integer, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class ReviewStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"

class ReviewContent(BaseModel):
    __tablename__ = "review_contents"

    application_id = Column(Integer, ForeignKey("campaign_applications.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(Text)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.DRAFT)
    published_at = Column(DateTime, nullable=True)
    post_url = Column(String, nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)

    # Relationships
    application = relationship("CampaignApplication", back_populates="review_contents")
    user = relationship("User", back_populates="review_contents")
    images = relationship("ReviewImage", back_populates="content")
    hashtags = relationship("ContentHashtag", back_populates="content") 