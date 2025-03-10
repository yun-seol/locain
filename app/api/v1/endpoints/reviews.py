from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserType
from app.models.review import ReviewContent, ReviewImage, ReviewStatus
from app.models.campaign import CampaignApplication
from app.schemas.review import (
    ReviewContentCreate,
    ReviewContentUpdate,
    ReviewContentResponse,
    ReviewContentList,
    ReviewImageCreate,
    ReviewImageUpdate,
    ReviewImageResponse,
    ReviewImageList,
    ReviewStats
)
from app.db.database import get_db
from datetime import datetime
import aiofiles
import os

router = APIRouter()

@router.post("/", response_model=ReviewContentResponse)
async def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: ReviewContentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    새로운 리뷰를 생성합니다.
    """
    if current_user.user_type != UserType.INFLUENCER:
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 리뷰를 작성할 수 있습니다.",
        )
    
    # 캠페인 신청 확인
    application = db.query(CampaignApplication).filter(
        CampaignApplication.id == review_in.campaign_application_id,
        CampaignApplication.influencer_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=404,
            detail="캠페인 신청을 찾을 수 없습니다.",
        )
    
    # 이미 리뷰가 작성되었는지 확인
    existing_review = db.query(ReviewContent).filter(
        ReviewContent.campaign_application_id == review_in.campaign_application_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="이미 리뷰가 작성되었습니다.",
        )
    
    review = ReviewContent(
        **review_in.dict(),
        influencer_id=current_user.id,
        status=ReviewStatus.PENDING
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/", response_model=ReviewContentList)
def read_reviews(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[ReviewStatus] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    리뷰 목록을 조회합니다.
    """
    query = db.query(ReviewContent)
    
    if current_user.user_type == UserType.INFLUENCER:
        query = query.filter(ReviewContent.influencer_id == current_user.id)
    elif current_user.user_type == UserType.BRAND:
        query = query.join(CampaignApplication).filter(
            CampaignApplication.brand_id == current_user.id
        )
    
    if status:
        query = query.filter(ReviewContent.status == status)
    
    total = query.count()
    reviews = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": reviews
    }

@router.get("/{review_id}", response_model=ReviewContentResponse)
def read_review(
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 리뷰의 정보를 조회합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    
    if current_user.user_type == UserType.INFLUENCER and review.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 리뷰에 대한 접근 권한이 없습니다.",
        )
    
    return review

@router.put("/{review_id}", response_model=ReviewContentResponse)
def update_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    review_in: ReviewContentUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 리뷰의 정보를 수정합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    
    if review.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 리뷰를 수정할 권한이 없습니다.",
        )
    
    if review.status == ReviewStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail="승인된 리뷰는 수정할 수 없습니다.",
        )
    
    update_data = review_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)
    
    review.updated_at = datetime.now()
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.delete("/{review_id}")
def delete_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 리뷰를 삭제합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    
    if review.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 리뷰를 삭제할 권한이 없습니다.",
        )
    
    if review.status == ReviewStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail="승인된 리뷰는 삭제할 수 없습니다.",
        )
    
    db.delete(review)
    db.commit()
    return {"message": "리뷰가 삭제되었습니다."}

@router.post("/{review_id}/feedback", response_model=ReviewContentResponse)
def create_review_feedback(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    feedback: str,
    rating: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    리뷰에 대한 브랜드 피드백을 작성합니다.
    """
    if current_user.user_type != UserType.BRAND:
        raise HTTPException(
            status_code=403,
            detail="브랜드만 피드백을 작성할 수 있습니다.",
        )
    
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    
    application = review.campaign_application
    if application.brand_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 리뷰에 대한 피드백을 작성할 권한이 없습니다.",
        )
    
    review.brand_feedback = feedback
    review.brand_rating = rating
    review.status = ReviewStatus.APPROVED
    review.updated_at = datetime.now()
    
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.post("/{review_id}/images", response_model=ReviewImageResponse)
async def upload_review_image(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    file: UploadFile = File(...),
    caption: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    리뷰 이미지를 업로드합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    
    if review.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 리뷰에 이미지를 업로드할 권한이 없습니다.",
        )
    
    # 이미지 저장 로직
    upload_dir = "uploads/reviews"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{review_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
    file_path = os.path.join(upload_dir, file_name)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # 이미지 정보 저장
    image = ReviewImage(
        review_content_id=review_id,
        image_url=file_path,
        caption=caption,
        order=len(review.images)
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.get("/{review_id}/stats", response_model=ReviewStats)
def get_review_stats(
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    리뷰 통계 정보를 조회합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=404,
            detail="리뷰를 찾을 수 없습니다.",
        )
    
    if review.influencer_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="해당 리뷰의 통계 정보를 조회할 권한이 없습니다.",
        )
    
    # TODO: 실제 통계 데이터 계산 로직 구현
    stats = ReviewStats(
        total_reviews=1,
        average_rating=review.rating,
        total_views=review.views,
        total_likes=review.likes,
        total_comments=review.comments,
        total_shares=review.shares,
        average_engagement_rate=0.0,  # 계산 로직 필요
        last_updated=review.updated_at
    )
    
    return stats 