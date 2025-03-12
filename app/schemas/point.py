from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.point import PointType

class PointBase(BaseModel):
    amount: float = Field(..., description="포인트 금액")
    description: str = Field(..., description="포인트 내역 설명")
    campaign_id: Optional[int] = Field(None, description="연결된 캠페인 ID")
    review_id: Optional[int] = Field(None, description="연결된 리뷰 ID")
    expires_at: Optional[datetime] = Field(None, description="만료일")

class PointCreate(PointBase):
    pass

class PointUse(BaseModel):
    amount: float = Field(..., gt=0, description="사용할 포인트 금액")
    description: str = Field(..., description="사용 내역 설명")
    campaign_id: Optional[int] = Field(None, description="연결된 캠페인 ID")

class PointRefund(BaseModel):
    point_id: int = Field(..., description="환불할 포인트 거래 ID")
    reason: str = Field(..., description="환불 사유")

class PointResponse(PointBase):
    id: int
    user_id: int
    balance: float
    type: PointType
    created_at: datetime

    class Config:
        from_attributes = True

class PointExchange(BaseModel):
    """포인트 환전 요청"""
    amount: float = Field(..., gt=0, description="환전할 포인트 금액")
    bank_name: str = Field(..., description="은행명")
    account_number: str = Field(..., description="계좌번호")
    account_holder: str = Field(..., description="예금주")

class PointExchangeResponse(BaseModel):
    """포인트 환전 응답"""
    id: int
    user_id: int
    amount: float
    status: str
    bank_name: str
    account_number: str
    account_holder: str
    requested_at: datetime
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class PointStats(BaseModel):
    """포인트 통계 정보"""
    total_earned: float = Field(..., description="총 적립 포인트")
    total_used: float = Field(..., description="총 사용 포인트")
    total_refunded: float = Field(..., description="총 환불 포인트")
    total_exchanged: float = Field(..., description="총 환전 포인트")
    current_balance: float = Field(..., description="현재 잔액")
    expiring_soon: float = Field(..., description="곧 만료될 포인트")
    expired: float = Field(..., description="만료된 포인트") 