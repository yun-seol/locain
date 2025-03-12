from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserType
from app.models.review import ReviewContent, ReviewImage, ReviewStatus
from app.models.campaign import CampaignApplication
from app.models.point import Point, PointType
from app.schemas.review import (
    ReviewContentCreate,
    ReviewContentUpdate,
    ReviewContentResponse,
    ReviewContentList,
    ReviewImageCreate,
    ReviewImageUpdate,
    ReviewImageResponse,
    ReviewImageList,
    ReviewStats,
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)
from app.db.database import get_db
from datetime import datetime
import aiofiles
import os

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    새로운 리뷰를 생성합니다.
    """
    if current_user.user_type != UserType.INFLUENCER:
        raise HTTPException(status_code=403, detail="인플루언서만 리뷰를 작성할 수 있습니다.")
    
    review = ReviewContent(
        **review_in.dict(),
        influencer_id=current_user.id,
        status=ReviewStatus.DRAFT
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    review_in: ReviewUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    리뷰를 수정합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    if review.influencer_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="리뷰를 수정할 권한이 없습니다.")
    
    if review.status not in [ReviewStatus.DRAFT, ReviewStatus.REJECTED]:
        raise HTTPException(status_code=400, detail="초안 또는 거절된 상태의 리뷰만 수정할 수 있습니다.")
    
    for field, value in review_in.dict(exclude_unset=True).items():
        setattr(review, field, value)
    
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.post("/{review_id}/submit", response_model=ReviewResponse)
def submit_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    리뷰를 제출합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    if review.influencer_id != current_user.id:
        raise HTTPException(status_code=403, detail="리뷰를 제출할 권한이 없습니다.")
    
    if review.status not in [ReviewStatus.DRAFT, ReviewStatus.REJECTED]:
        raise HTTPException(status_code=400, detail="초안 또는 거절된 상태의 리뷰만 제출할 수 있습니다.")
    
    review.status = ReviewStatus.SUBMITTED
    review.submission_date = datetime.utcnow()
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.post("/{review_id}/approve", response_model=ReviewResponse)
def approve_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    리뷰를 승인합니다. (관리자 또는 브랜드 전용)
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    campaign = review.campaign
    if current_user.user_type != UserType.ADMIN and campaign.brand_id != current_user.id:
        raise HTTPException(status_code=403, detail="리뷰를 승인할 권한이 없습니다.")
    
    if review.status != ReviewStatus.SUBMITTED:
        raise HTTPException(status_code=400, detail="제출된 상태의 리뷰만 승인할 수 있습니다.")
    
    review.status = ReviewStatus.APPROVED
    review.approval_date = datetime.utcnow()
    db.add(review)
    
    # 포인트 적립
    point = Point(
        user_id=review.influencer_id,
        amount=campaign.reward_amount,
        type=PointType.EARN,
        description=f"리뷰 승인 보상: {campaign.title}",
        campaign_id=campaign.id,
        review_id=review.id,
        expires_at=datetime.utcnow().replace(year=datetime.utcnow().year + 1)  # 1년 후 만료
    )
    db.add(point)
    
    db.commit()
    db.refresh(review)
    return review

@router.post("/{review_id}/reject", response_model=ReviewResponse)
def reject_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    rejection_reason: str,
    required_modifications: str = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    리뷰를 거절합니다. (관리자 또는 브랜드 전용)
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    campaign = review.campaign
    if current_user.user_type != UserType.ADMIN and campaign.brand_id != current_user.id:
        raise HTTPException(status_code=403, detail="리뷰를 거절할 권한이 없습니다.")
    
    if review.status != ReviewStatus.SUBMITTED:
        raise HTTPException(status_code=400, detail="제출된 상태의 리뷰만 거절할 수 있습니다.")
    
    review.status = ReviewStatus.REJECTED
    review.rejection_reason = rejection_reason
    review.required_modifications = required_modifications
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.post("/{review_id}/complete", response_model=ReviewResponse)
def complete_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    platform_url: str,
    views: int = 0,
    likes: int = 0,
    comments: int = 0,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    리뷰를 완료 처리합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    if review.influencer_id != current_user.id:
        raise HTTPException(status_code=403, detail="리뷰를 완료 처리할 권한이 없습니다.")
    
    if review.status != ReviewStatus.APPROVED:
        raise HTTPException(status_code=400, detail="승인된 상태의 리뷰만 완료 처리할 수 있습니다.")
    
    review.status = ReviewStatus.COMPLETED
    review.platform_url = platform_url
    review.views = views
    review.likes = likes
    review.comments = comments
    review.completion_date = datetime.utcnow()
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/", response_model=List[ReviewResponse])
def read_reviews(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    campaign_id: int = None,
    status: ReviewStatus = None
) -> Any:
    """
    리뷰 목록을 조회합니다.
    """
    query = db.query(ReviewContent)
    
    if current_user.user_type == UserType.INFLUENCER:
        query = query.filter(ReviewContent.influencer_id == current_user.id)
    elif current_user.user_type == UserType.BRAND:
        query = query.join(ReviewContent.campaign).filter(ReviewContent.campaign.has(brand_id=current_user.id))
    
    if campaign_id:
        query = query.filter(ReviewContent.campaign_id == campaign_id)
    if status:
        query = query.filter(ReviewContent.status == status)
    
    reviews = query.order_by(ReviewContent.id.desc()).offset(skip).limit(limit).all()
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def read_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    특정 리뷰를 조회합니다.
    """
    review = db.query(ReviewContent).filter(ReviewContent.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    if (current_user.user_type == UserType.INFLUENCER and review.influencer_id != current_user.id) or \
       (current_user.user_type == UserType.BRAND and review.campaign.brand_id != current_user.id):
        raise HTTPException(status_code=403, detail="리뷰를 조회할 권한이 없습니다.")
    
    return review

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