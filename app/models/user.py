from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserType(str, Enum):
    ADMIN = "admin"
    BRAND = "brand"
    INFLUENCER = "influencer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    role = Column(SQLEnum(UserType))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaigns = relationship("Campaign", back_populates="user")
    campaign_applications = relationship("CampaignApplication", back_populates="user")
    review_contents = relationship("ReviewContent", back_populates="influencer")
    payments_as_brand = relationship("Payment", foreign_keys="Payment.brand_id", back_populates="brand")
    payments_as_influencer = relationship("Payment", foreign_keys="Payment.influencer_id", back_populates="influencer")
    social_channels = relationship("SocialChannel", back_populates="user") 