from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserType
from app.models.coupon import Coupon, CouponStatus, CouponType
from app.schemas.coupon import (
    CouponCreate, CouponUpdate, CouponResponse, CouponUse,
    CouponBatchCreate, CouponStats
)
from app.db.database import get_db
import random
import string

router = APIRouter()

def generate_coupon_code(prefix: str = "") -> str:
    """랜덤 쿠폰 코드를 생성합니다."""
    chars = string.ascii_uppercase + string.digits
    random_str = ''.join(random.choice(chars) for _ in range(12))
    return f"{prefix}{random_str}"

@router.post("/", response_model=CouponResponse)
def create_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_in: CouponCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    새로운 쿠폰을 생성합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    coupon = Coupon(**coupon_in.dict())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@router.get("/", response_model=List[CouponResponse])
def read_coupons(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    쿠폰 목록을 조회합니다.
    """
    if current_user.user_type == UserType.ADMIN:
        coupons = db.query(Coupon).offset(skip).limit(limit).all()
    else:
        coupons = db.query(Coupon).filter(Coupon.user_id == current_user.id).offset(skip).limit(limit).all()
    return coupons

@router.post("/use", response_model=CouponResponse)
def use_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_in: CouponUse,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    쿠폰을 사용합니다.
    """
    coupon = db.query(Coupon).filter(
        Coupon.code == coupon_in.code,
        Coupon.user_id == current_user.id,
        Coupon.status == CouponStatus.ACTIVE
    ).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="유효한 쿠폰을 찾을 수 없습니다.")
    
    if coupon.end_date < datetime.utcnow():
        coupon.status = CouponStatus.EXPIRED
        db.add(coupon)
        db.commit()
        raise HTTPException(status_code=400, detail="만료된 쿠폰입니다.")
    
    if coupon.min_purchase_amount and coupon_in.purchase_amount < coupon.min_purchase_amount:
        raise HTTPException(status_code=400, detail=f"최소 구매 금액({coupon.min_purchase_amount}원)을 만족하지 않습니다.")
    
    coupon.status = CouponStatus.USED
    coupon.used_at = datetime.utcnow()
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@router.post("/{coupon_id}/cancel", response_model=CouponResponse)
def cancel_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    쿠폰 사용을 취소합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="쿠폰을 찾을 수 없습니다.")
    
    if coupon.status != CouponStatus.USED:
        raise HTTPException(status_code=400, detail="사용된 쿠폰만 취소할 수 있습니다.")
    
    coupon.status = CouponStatus.ACTIVE
    coupon.used_at = None
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@router.post("/batch", response_model=List[CouponResponse])
def create_coupon_batch(
    *,
    db: Session = Depends(get_db),
    batch_in: CouponBatchCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    대량 쿠폰을 생성합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    coupons = []
    for _ in range(batch_in.quantity):
        coupon = Coupon(
            code=generate_coupon_code(batch_in.prefix),
            type=batch_in.type,
            value=batch_in.value,
            min_purchase_amount=batch_in.min_purchase_amount,
            max_discount_amount=batch_in.max_discount_amount,
            start_date=batch_in.start_date,
            end_date=batch_in.end_date,
            campaign_id=batch_in.campaign_id,
            status=CouponStatus.ACTIVE
        )
        coupons.append(coupon)
    
    db.bulk_save_objects(coupons)
    db.commit()
    
    # 생성된 쿠폰 조회
    created_coupons = db.query(Coupon).filter(
        Coupon.code.like(f"{batch_in.prefix}%")
    ).order_by(Coupon.id.desc()).limit(batch_in.quantity).all()
    
    return created_coupons

@router.post("/assign/{coupon_id}", response_model=CouponResponse)
def assign_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_id: int,
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    쿠폰을 특정 사용자에게 할당합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="쿠폰을 찾을 수 없습니다.")
    
    if coupon.user_id:
        raise HTTPException(status_code=400, detail="이미 할당된 쿠폰입니다.")
    
    coupon.user_id = user_id
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@router.post("/validate", response_model=CouponResponse)
def validate_coupon(
    *,
    db: Session = Depends(get_db),
    code: str,
    purchase_amount: float,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    쿠폰의 유효성을 검사합니다.
    """
    coupon = db.query(Coupon).filter(
        Coupon.code == code,
        Coupon.status == CouponStatus.ACTIVE
    ).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="유효한 쿠폰을 찾을 수 없습니다.")
    
    if coupon.user_id and coupon.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="이 쿠폰을 사용할 권한이 없습니다.")
    
    if coupon.end_date < datetime.utcnow():
        coupon.status = CouponStatus.EXPIRED
        db.add(coupon)
        db.commit()
        raise HTTPException(status_code=400, detail="만료된 쿠폰입니다.")
    
    if coupon.min_purchase_amount and purchase_amount < coupon.min_purchase_amount:
        raise HTTPException(
            status_code=400,
            detail=f"최소 구매 금액({coupon.min_purchase_amount}원)을 만족하지 않습니다."
        )
    
    return coupon

@router.get("/stats", response_model=CouponStats)
def get_coupon_stats(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    쿠폰 통계 정보를 조회합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    total_issued = db.query(Coupon).count()
    total_used = db.query(Coupon).filter(Coupon.status == CouponStatus.USED).count()
    total_active = db.query(Coupon).filter(Coupon.status == CouponStatus.ACTIVE).count()
    total_expired = db.query(Coupon).filter(Coupon.status == CouponStatus.EXPIRED).count()
    total_cancelled = db.query(Coupon).filter(Coupon.status == CouponStatus.CANCELLED).count()
    
    usage_rate = (total_used / total_issued * 100) if total_issued > 0 else 0
    
    return CouponStats(
        total_issued=total_issued,
        total_used=total_used,
        total_active=total_active,
        total_expired=total_expired,
        total_cancelled=total_cancelled,
        usage_rate=usage_rate
    )

@router.get("/campaign/{campaign_id}", response_model=List[CouponResponse])
def get_campaign_coupons(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    특정 캠페인의 쿠폰 목록을 조회합니다.
    """
    if current_user.user_type != UserType.ADMIN:
        coupons = db.query(Coupon).filter(
            Coupon.campaign_id == campaign_id,
            Coupon.user_id == current_user.id
        ).all()
    else:
        coupons = db.query(Coupon).filter(
            Coupon.campaign_id == campaign_id
        ).all()
    
    return coupons 