from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base_class import Base

class PointExchangeStatus(str, Enum):
    PENDING = "pending"  # 처리 대기
    APPROVED = "approved"  # 승인됨
    REJECTED = "rejected"  # 거절됨
    COMPLETED = "completed"  # 완료됨
    CANCELLED = "cancelled"  # 취소됨

class PointExchange(Base):
    __tablename__ = "point_exchanges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)  # 환전 금액
    status = Column(SQLEnum(PointExchangeStatus), default=PointExchangeStatus.PENDING)
    bank_name = Column(String)  # 은행명
    account_number = Column(String)  # 계좌번호
    account_holder = Column(String)  # 예금주
    requested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)  # 처리 완료 시간
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 처리자 ID
    rejection_reason = Column(String, nullable=True)  # 거절 사유
    transaction_id = Column(String, nullable=True)  # 실제 송금 거래 ID
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="point_exchanges")
    processor = relationship("User", foreign_keys=[processed_by], backref="processed_exchanges") 