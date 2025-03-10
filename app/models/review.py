from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum as SQLEnum, DateTime, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ReviewContent(Base):
    __tablename__ = "review_contents"

    id = Column(Integer, primary_key=True, index=True)
    campaign_application_id = Column(Integer, ForeignKey("campaign_applications.id"))
    influencer_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    rating = Column(Integer)
    hashtags = Column(JSON)  # JSON array
    images = Column(JSON)  # JSON array
    platform = Column(String)
    post_url = Column(String)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    status = Column(SQLEnum(ReviewStatus))
    brand_feedback = Column(String)
    brand_rating = Column(Integer)
    brand_comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaign_application = relationship("CampaignApplication", back_populates="review_contents")
    influencer = relationship("User", back_populates="review_contents")
    images_list = relationship("ReviewImage", back_populates="review_content")

class ReviewImage(Base):
    __tablename__ = "review_images"

    id = Column(Integer, primary_key=True, index=True)
    review_content_id = Column(Integer, ForeignKey("review_contents.id"))
    image_url = Column(String)
    caption = Column(String)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    review_content = relationship("ReviewContent", back_populates="images_list") 