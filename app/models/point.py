from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base_class import Base

class PointType(str, Enum):
    """포인트 거래 유형"""
    EARN = "EARN"          # 적립
    USE = "USE"            # 사용
    REFUND = "REFUND"      # 환불
    EXCHANGE = "EXCHANGE"  # 환전

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(SQLEnum(PointType), nullable=False)
    description = Column(String, nullable=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="points")
    campaign = relationship("Campaign", back_populates="points")
    review = relationship("Review", back_populates="points") 