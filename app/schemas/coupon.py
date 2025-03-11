from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.coupon import CouponType, CouponStatus

class CouponBase(BaseModel):
    code: str = Field(..., description="쿠폰 코드")
    type: CouponType = Field(..., description="쿠폰 타입 (정액/정률)")
    value: float = Field(..., description="할인 금액 또는 비율")
    min_purchase_amount: Optional[float] = Field(None, description="최소 구매 금액")
    max_discount_amount: Optional[float] = Field(None, description="최대 할인 금액 (정률 할인시)")
    start_date: datetime = Field(..., description="사용 시작일")
    end_date: datetime = Field(..., description="사용 종료일")
    campaign_id: Optional[int] = Field(None, description="연결된 캠페인 ID")

class CouponCreate(CouponBase):
    user_id: Optional[int] = Field(None, description="쿠폰을 발급받을 사용자 ID")
    quantity: Optional[int] = Field(1, description="발급할 쿠폰 수량")

class CouponUpdate(BaseModel):
    status: Optional[CouponStatus] = Field(None, description="쿠폰 상태")
    end_date: Optional[datetime] = Field(None, description="사용 종료일 변경")

class CouponUse(BaseModel):
    code: str = Field(..., description="사용할 쿠폰 코드")
    purchase_amount: float = Field(..., description="구매 금액")

class CouponResponse(CouponBase):
    id: int
    status: CouponStatus
    user_id: Optional[int]
    used_at: Optional[datetime]

    class Config:
        from_attributes = True

class CouponBatchCreate(BaseModel):
    """대량 쿠폰 생성 요청"""
    prefix: str = Field(..., description="쿠폰 코드 접두사")
    quantity: int = Field(..., ge=1, le=1000, description="생성할 쿠폰 수량")
    type: CouponType
    value: float
    min_purchase_amount: Optional[float]
    max_discount_amount: Optional[float]
    start_date: datetime
    end_date: datetime
    campaign_id: Optional[int]

class CouponStats(BaseModel):
    """쿠폰 통계 정보"""
    total_issued: int = Field(..., description="총 발행 수")
    total_used: int = Field(..., description="총 사용 수")
    total_active: int = Field(..., description="활성 상태 수")
    total_expired: int = Field(..., description="만료된 수")
    total_cancelled: int = Field(..., description="취소된 수")
    usage_rate: float = Field(..., description="사용률") 