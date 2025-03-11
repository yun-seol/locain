from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base_class import Base

class PointTransactionType(str, Enum):
    EARN = "earn"  # 적립
    USE = "use"  # 사용
    REFUND = "refund"  # 환불
    EXPIRE = "expire"  # 만료
    CANCEL = "cancel"  # 취소

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)  # 포인트 금액
    balance = Column(Float)  # 잔액
    type = Column(SQLEnum(PointTransactionType))
    description = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    review_id = Column(Integer, ForeignKey("review_contents.id"), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="points")
    campaign = relationship("Campaign", back_populates="points")
    review = relationship("ReviewContent", back_populates="points") 