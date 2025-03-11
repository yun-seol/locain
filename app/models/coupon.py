from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base_class import Base

class CouponType(str, Enum):
    FIXED = "fixed"  # 정액 할인
    PERCENTAGE = "percentage"  # 정률 할인

class CouponStatus(str, Enum):
    ACTIVE = "active"  # 사용 가능
    USED = "used"  # 사용됨
    EXPIRED = "expired"  # 만료됨
    CANCELLED = "cancelled"  # 취소됨

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    type = Column(SQLEnum(CouponType))
    value = Column(Float)  # 할인 금액 또는 비율
    min_purchase_amount = Column(Float, nullable=True)  # 최소 구매 금액
    max_discount_amount = Column(Float, nullable=True)  # 최대 할인 금액 (정률 할인시)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(SQLEnum(CouponStatus), default=CouponStatus.ACTIVE)
    user_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    used_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="coupons")
    campaign = relationship("Campaign", back_populates="coupons") 