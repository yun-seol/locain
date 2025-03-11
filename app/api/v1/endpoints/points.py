from typing import Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.user import User, UserType
from app.models.point import Point, PointType
from app.models.point_exchange import PointExchange, PointExchangeStatus
from app.schemas.point import (
    PointCreate, PointUse, PointRefund, PointResponse,
    PointExchange as PointExchangeSchema, PointExchangeResponse,
    PointStats
)
from app.db.database import get_db

router = APIRouter()

@router.post("/earn", response_model=PointResponse)
def earn_points(
    *,
    db: Session = Depends(get_db),
    point_in: PointCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    포인트를 적립합니다.
    """
    point = Point(
        user_id=current_user.id,
        amount=point_in.amount,
        type=PointType.EARN,
        description=point_in.description,
        campaign_id=point_in.campaign_id,
        review_id=point_in.review_id,
        expires_at=point_in.expires_at or datetime.utcnow() + timedelta(days=365)
    )
    
    db.add(point)
    db.commit()
    db.refresh(point)
    return point

@router.post("/use", response_model=PointResponse)
def use_points(
    *,
    db: Session = Depends(get_db),
    point_in: PointUse,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    포인트를 사용합니다.
    """
    # 현재 사용 가능한 포인트 잔액 계산
    available_points = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.expires_at > datetime.utcnow(),
        Point.type == PointType.EARN
    ).scalar() or 0
    
    used_points = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type.in_([PointType.USE, PointType.EXCHANGE])
    ).scalar() or 0
    
    current_balance = available_points - used_points
    
    if current_balance < point_in.amount:
        raise HTTPException(
            status_code=400,
            detail=f"포인트가 부족합니다. (현재 잔액: {current_balance})"
        )
    
    point = Point(
        user_id=current_user.id,
        amount=-point_in.amount,
        type=PointType.USE,
        description=point_in.description,
        campaign_id=point_in.campaign_id
    )
    
    db.add(point)
    db.commit()
    db.refresh(point)
    return point

@router.post("/refund/{point_id}", response_model=PointResponse)
def refund_points(
    *,
    db: Session = Depends(get_db),
    point_id: int,
    refund_in: PointRefund,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    사용한 포인트를 환불합니다.
    """
    point = db.query(Point).filter(Point.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="포인트 내역을 찾을 수 없습니다.")
    
    if point.user_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    if point.type != PointType.USE:
        raise HTTPException(status_code=400, detail="사용한 포인트만 환불할 수 있습니다.")
    
    refund = Point(
        user_id=point.user_id,
        amount=-point.amount,  # 사용한 포인트의 반대 값
        type=PointType.REFUND,
        description=refund_in.reason,
        campaign_id=point.campaign_id
    )
    
    db.add(refund)
    db.commit()
    db.refresh(refund)
    return refund

@router.post("/exchange", response_model=PointExchangeResponse)
def request_exchange(
    *,
    db: Session = Depends(get_db),
    exchange_in: PointExchangeSchema,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    포인트 환전을 요청합니다.
    """
    # 현재 사용 가능한 포인트 잔액 계산
    available_points = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.expires_at > datetime.utcnow(),
        Point.type == PointType.EARN
    ).scalar() or 0
    
    used_points = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type.in_([PointType.USE, PointType.EXCHANGE])
    ).scalar() or 0
    
    current_balance = available_points - used_points
    
    if current_balance < exchange_in.amount:
        raise HTTPException(
            status_code=400,
            detail=f"포인트가 부족합니다. (현재 잔액: {current_balance})"
        )
    
    if exchange_in.amount < 10000:  # 최소 환전 금액
        raise HTTPException(
            status_code=400,
            detail="최소 환전 금액은 10,000포인트입니다."
        )
    
    # 포인트 환전 요청 생성
    exchange = PointExchange(
        user_id=current_user.id,
        amount=exchange_in.amount,
        status=PointExchangeStatus.PENDING,
        bank_name=exchange_in.bank_name,
        account_number=exchange_in.account_number,
        account_holder=exchange_in.account_holder,
        requested_at=datetime.utcnow()
    )
    
    # 포인트 차감
    point = Point(
        user_id=current_user.id,
        amount=-exchange_in.amount,
        type=PointType.EXCHANGE,
        description=f"포인트 환전 신청 (은행: {exchange_in.bank_name})"
    )
    
    db.add(exchange)
    db.add(point)
    db.commit()
    db.refresh(exchange)
    return exchange

@router.get("/stats", response_model=PointStats)
def get_point_stats(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    포인트 통계 정보를 조회합니다.
    """
    earned = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type == PointType.EARN
    ).scalar() or 0
    
    used = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type == PointType.USE
    ).scalar() or 0
    
    refunded = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type == PointType.REFUND
    ).scalar() or 0
    
    exchanged = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type == PointType.EXCHANGE
    ).scalar() or 0
    
    # 현재 잔액 계산
    current_balance = earned + used + refunded + exchanged
    
    # 30일 이내 만료 예정인 포인트
    expiring_soon = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type == PointType.EARN,
        Point.expires_at.between(
            datetime.utcnow(),
            datetime.utcnow() + timedelta(days=30)
        )
    ).scalar() or 0
    
    # 만료된 포인트
    expired = db.query(func.sum(Point.amount)).filter(
        Point.user_id == current_user.id,
        Point.type == PointType.EARN,
        Point.expires_at < datetime.utcnow()
    ).scalar() or 0
    
    return PointStats(
        total_earned=earned,
        total_used=-used if used else 0,
        total_refunded=refunded,
        total_exchanged=-exchanged if exchanged else 0,
        current_balance=current_balance,
        expiring_soon=expiring_soon,
        expired=expired
    ) 