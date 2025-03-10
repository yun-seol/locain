from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.models.payment import PaymentStatus

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_PAYMENT = "mobile_payment"
    VIRTUAL_ACCOUNT = "virtual_account"

class PaymentBase(BaseModel):
    amount: float
    currency: str = "KRW"
    payment_method: PaymentMethod
    description: str
    campaign_application_id: int
    transaction_id: Optional[str] = None
    status: PaymentStatus = PaymentStatus.PENDING
    refund_status: Optional[str] = None
    refund_amount: Optional[float] = None
    refund_reason: Optional[str] = None
    refund_date: Optional[datetime] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    brand_id: int
    influencer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentResponse(PaymentBase):
    id: int
    brand_id: int
    influencer_id: int
    status: PaymentStatus
    transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    refund_amount: Optional[int] = None
    refund_reason: Optional[str] = None
    refund_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaymentInDB(PaymentResponse):
    pass

class PaymentList(BaseModel):
    total: int
    items: List[PaymentResponse]

    class Config:
        from_attributes = True

class PaymentStats(BaseModel):
    total_amount: float
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    payment_method: str
    transaction_id: Optional[str] = None
    refund_status: Optional[str] = None
    refund_amount: Optional[float] = None
    refund_reason: Optional[str] = None
    refund_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class RefundRequest(BaseModel):
    amount: int
    reason: str

class PaymentWebhook(BaseModel):
    payment_id: int
    status: PaymentStatus
    transaction_id: str
    payment_date: datetime
    amount: int
    currency: str
    payment_method: PaymentMethod
    metadata: Optional[dict] = None 