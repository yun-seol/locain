from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum
from datetime import datetime

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    campaign_application_id = Column(Integer, ForeignKey("campaign_applications.id"))
    brand_id = Column(Integer, ForeignKey("users.id"))
    influencer_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String, unique=True, nullable=True)
    payment_date = Column(DateTime, nullable=True)
    refund_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaign_application = relationship("CampaignApplication", back_populates="payment")
    brand = relationship("User", foreign_keys=[brand_id], back_populates="payments_as_brand")
    influencer = relationship("User", foreign_keys=[influencer_id], back_populates="payments_as_influencer") 