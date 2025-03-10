from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class CampaignApplication(BaseModel):
    __tablename__ = "campaign_applications"

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    application_text = Column(Text)

    # Relationships
    campaign = relationship("Campaign", back_populates="applications")
    user = relationship("User", back_populates="campaign_applications") 