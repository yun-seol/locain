from typing import Any, List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserType
from app.models.payment import Payment, PaymentStatus
from app.models.campaign import CampaignApplication
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
    PaymentList,
    PaymentStats,
    RefundRequest,
    PaymentWebhook
)
from app.core.payment import (
    IamportPayment,
    process_payment_with_retry,
    send_webhook_with_retry,
    calculate_payment_stats
)
from app.db.database import get_db
from datetime import datetime
import httpx
from app.core.config import settings
import logging
from app import crud, schemas
from app.core.security import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=PaymentResponse)
async def create_payment(
    payment_in: PaymentCreate,
    payment_method_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> Any:
    """
    새로운 결제를 생성합니다.
    """
    if current_user.user_type != UserType.BRAND:
        raise HTTPException(
            status_code=403,
            detail="브랜드만 결제를 생성할 수 있습니다.",
        )
    
    # 캠페인 신청 확인
    application = db.query(CampaignApplication).filter(
        CampaignApplication.id == payment_in.campaign_application_id,
        CampaignApplication.brand_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=404,
            detail="캠페인 신청을 찾을 수 없습니다.",
        )
    
    # 이미 결제가 생성되었는지 확인
    existing_payment = db.query(Payment).filter(
        Payment.campaign_application_id == payment_in.campaign_application_id
    ).first()
    
    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="이미 결제가 생성되었습니다.",
        )
    
    payment = Payment(
        **payment_in.dict(),
        brand_id=current_user.id,
        influencer_id=application.influencer_id,
        status=PaymentStatus.PENDING
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    # 결제 처리 시작
    background_tasks.add_task(process_payment_with_retry, db, payment, payment_method_data)
    
    return payment

@router.post("/webhook")
async def payment_webhook(
    request: Request,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> Any:
    """
    iamport 웹훅을 처리합니다.
    """
    try:
        # 웹훅 데이터 검증
        data = await request.json()
        if not data:
            raise HTTPException(
                status_code=400,
                detail="웹훅 데이터가 비어있습니다.",
            )
        
        # 필수 필드 검증
        required_fields = ["imp_uid", "merchant_uid", "status"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"필수 필드가 누락되었습니다: {', '.join(missing_fields)}",
            )
        
        imp_uid = data.get("imp_uid")
        merchant_uid = data.get("merchant_uid")
        status = data.get("status")
        
        # 결제 정보 조회
        try:
            payment_id = int(merchant_uid.split("_")[1])
        except (IndexError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="잘못된 merchant_uid 형식입니다.",
            )
        
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=404,
                detail="결제를 찾을 수 없습니다.",
            )
        
        # 결제 검증
        iamport = IamportPayment()
        try:
            if not await iamport.verify_payment(payment, imp_uid):
                raise HTTPException(
                    status_code=400,
                    detail="결제 검증에 실패했습니다.",
                )
        except Exception as e:
            logger.error(f"Payment verification failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="결제 검증 중 오류가 발생했습니다.",
            )
        
        # 결제 상태 업데이트
        try:
            if status == "paid":
                payment.status = PaymentStatus.COMPLETED
                payment.transaction_id = imp_uid
                payment.payment_date = datetime.now()
            elif status == "failed":
                payment.status = PaymentStatus.FAILED
            elif status == "cancelled":
                payment.status = PaymentStatus.REFUNDED
                payment.refund_date = datetime.now()
            
            payment.updated_at = datetime.now()
            db.add(payment)
            db.commit()
        except Exception as e:
            logger.error(f"Payment status update failed: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="결제 상태 업데이트 중 오류가 발생했습니다.",
            )
        
        # 웹훅 전송
        try:
            background_tasks.add_task(send_webhook_with_retry, payment)
        except Exception as e:
            logger.error(f"Webhook scheduling failed: {str(e)}")
            # 웹훅 전송 실패는 치명적이지 않으므로 계속 진행
        
        return {"message": "웹훅이 성공적으로 처리되었습니다."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="웹훅 처리 중 오류가 발생했습니다.",
        )

@router.get("/", response_model=PaymentList)
def read_payments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[PaymentStatus] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    결제 목록을 조회합니다.
    """
    query = db.query(Payment)
    
    if current_user.user_type == UserType.BRAND:
        query = query.filter(Payment.brand_id == current_user.id)
    elif current_user.user_type == UserType.INFLUENCER:
        query = query.filter(Payment.influencer_id == current_user.id)
    
    if status:
        query = query.filter(Payment.status == status)
    
    total = query.count()
    payments = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": payments
    }

@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(
    payment_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 결제의 정보를 조회합니다.
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=404,
            detail="결제를 찾을 수 없습니다.",
        )
    
    if current_user.user_type == UserType.BRAND and payment.brand_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 결제에 대한 접근 권한이 없습니다.",
        )
    
    if current_user.user_type == UserType.INFLUENCER and payment.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 결제에 대한 접근 권한이 없습니다.",
        )
    
    return payment

@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_payment(
    *,
    db: Session = Depends(get_db),
    payment_id: int,
    refund_in: RefundRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    결제를 환불합니다.
    """
    try:
        # 권한 검증
        if current_user.user_type != UserType.BRAND:
            raise HTTPException(
                status_code=403,
                detail="브랜드만 환불을 처리할 수 있습니다.",
            )
        
        # 결제 정보 조회
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=404,
                detail="결제를 찾을 수 없습니다.",
            )
        
        # 소유권 검증
        if payment.brand_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="해당 결제를 환불할 권한이 없습니다.",
            )
        
        # 결제 상태 검증
        if payment.status != PaymentStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail="완료된 결제만 환불할 수 있습니다.",
            )
        
        # 환불 금액 검증
        if refund_in.amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="환불 금액은 0보다 커야 합니다.",
            )
        
        if refund_in.amount > payment.amount:
            raise HTTPException(
                status_code=400,
                detail="환불 금액이 결제 금액을 초과할 수 없습니다.",
            )
        
        # 환불 계좌 정보 검증
        if not all([payment.refund_bank, payment.refund_account]):
            raise HTTPException(
                status_code=400,
                detail="환불 계좌 정보가 누락되었습니다.",
            )
        
        # iamport 환불 처리
        iamport = IamportPayment()
        try:
            cancel_result = await iamport.cancel_payment(payment, refund_in.reason)
            
            # 환불 결과 검증
            if not cancel_result.get("success"):
                raise HTTPException(
                    status_code=400,
                    detail=f"환불 처리 실패: {cancel_result.get('message')}",
                )
            
            # 결제 상태 업데이트
            payment.status = PaymentStatus.REFUNDED
            payment.refund_amount = refund_in.amount
            payment.refund_reason = refund_in.reason
            payment.refund_date = datetime.now()
            payment.updated_at = datetime.now()
            
            db.add(payment)
            db.commit()
            db.refresh(payment)
            
            # 환불 웹훅 전송
            try:
                background_tasks.add_task(send_webhook_with_retry, payment)
            except Exception as e:
                logger.error(f"Refund webhook scheduling failed: {str(e)}")
                # 웹훅 전송 실패는 치명적이지 않으므로 계속 진행
            
            return payment
            
        except Exception as e:
            logger.error(f"Refund processing failed: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="환불 처리 중 오류가 발생했습니다.",
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in refund process: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="환불 처리 중 예상치 못한 오류가 발생했습니다.",
        )

@router.get("/{payment_id}/stats", response_model=PaymentStats)
def get_payment_stats(
    payment_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    결제 통계 정보를 조회합니다.
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=404,
            detail="결제를 찾을 수 없습니다.",
        )
    
    if payment.brand_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="해당 결제의 통계 정보를 조회할 권한이 없습니다.",
        )
    
    return calculate_payment_stats(db, payment)

@router.get("/me", response_model=List[schemas.Payment])
def read_user_payments(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    사용자의 결제 내역을 조회합니다.
    """
    return crud.payment.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )

@router.put("/{payment_id}", response_model=schemas.Payment)
def update_payment(
    payment_id: int,
    payment_in: schemas.PaymentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    """
    결제 정보를 업데이트합니다.
    """
    payment = crud.payment.get(db=db, id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.payment.update(db=db, db_obj=payment, obj_in=payment_in)

@router.post("/process", response_model=schemas.Payment)
def process_payment(
    payment_in: schemas.PaymentCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> Any:
    """
    새로운 결제를 처리합니다.
    """
    payment = crud.payment.create_with_user(
        db=db, obj_in=payment_in, user_id=current_user.id
    )
    background_tasks.add_task(
        crud.payment.process_payment,
        db=db,
        payment_id=payment.id
    )
    return payment 