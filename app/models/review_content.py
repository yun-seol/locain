from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base_class import Base

class ReviewStatus(str, Enum):
    DRAFT = "draft"  # 작성 중
    SUBMITTED = "submitted"  # 제출됨
    APPROVED = "approved"  # 승인됨
    REJECTED = "rejected"  # 거절됨
    COMPLETED = "completed"  # 완료됨

class ReviewContent(Base):
    __tablename__ = "review_contents"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    influencer_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    content = Column(Text)
    media_urls = Column(String)  # JSON 형식으로 저장된 미디어 URL 목록
    platform_url = Column(String)  # 실제 게시된 리뷰 URL
    status = Column(SQLEnum(ReviewStatus), default=ReviewStatus.DRAFT)
    submission_date = Column(DateTime, nullable=True)
    approval_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    rejection_reason = Column(String, nullable=True)
    required_modifications = Column(Text, nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="review_contents")
    influencer = relationship("User", back_populates="review_contents")
    points = relationship("Point", back_populates="review")
    images = relationship("ReviewImage", back_populates="content")
    hashtags = relationship("ContentHashtag", back_populates="content") 