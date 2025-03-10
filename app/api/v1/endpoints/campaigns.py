from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.models.user import User, UserType
from app.models.campaign import Campaign, CampaignStatus, CampaignApplication
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignList,
    CampaignApplicationCreate,
    CampaignApplicationUpdate,
    CampaignApplicationResponse,
    CampaignApplicationList
)
from app.db.database import get_db
from datetime import datetime
from app.core.security import get_current_active_user

router = APIRouter()

@router.post("/", response_model=CampaignResponse)
def create_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_in: CampaignCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    새로운 캠페인을 생성합니다.
    """
    if current_user.user_type != UserType.BRAND:
        raise HTTPException(
            status_code=403,
            detail="브랜드만 캠페인을 생성할 수 있습니다.",
        )
    
    if campaign_in.start_date < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="시작일은 현재 시간보다 이후여야 합니다.",
        )
    
    if campaign_in.end_date <= campaign_in.start_date:
        raise HTTPException(
            status_code=400,
            detail="종료일은 시작일보다 이후여야 합니다.",
        )
    
    campaign = Campaign(
        **campaign_in.dict(),
        brand_id=current_user.id,
        status=CampaignStatus.DRAFT
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.get("/", response_model=CampaignList)
def read_campaigns(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[CampaignStatus] = None,
    campaign_type: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    캠페인 목록을 조회합니다.
    """
    query = db.query(Campaign)
    
    if current_user.user_type == UserType.BRAND:
        query = query.filter(Campaign.brand_id == current_user.id)
    elif current_user.user_type == UserType.INFLUENCER:
        query = query.filter(Campaign.status == CampaignStatus.ACTIVE)
    
    if status:
        query = query.filter(Campaign.status == status)
    if campaign_type:
        query = query.filter(Campaign.campaign_type == campaign_type)
    
    total = query.count()
    campaigns = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": campaigns
    }

@router.get("/{campaign_id}", response_model=CampaignResponse)
def read_campaign(
    campaign_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 캠페인의 정보를 조회합니다.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="캠페인을 찾을 수 없습니다.",
        )
    
    if current_user.user_type == UserType.BRAND and campaign.brand_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 캠페인에 대한 접근 권한이 없습니다.",
        )
    
    return campaign

@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    campaign_in: CampaignUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 캠페인의 정보를 수정합니다.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="캠페인을 찾을 수 없습니다.",
        )
    
    if campaign.brand_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 캠페인을 수정할 권한이 없습니다.",
        )
    
    if campaign.status == CampaignStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="완료된 캠페인은 수정할 수 없습니다.",
        )
    
    update_data = campaign_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{campaign_id}")
def delete_campaign(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 캠페인을 삭제합니다.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="캠페인을 찾을 수 없습니다.",
        )
    
    if campaign.brand_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 캠페인을 삭제할 권한이 없습니다.",
        )
    
    if campaign.status != CampaignStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail="초안 상태의 캠페인만 삭제할 수 있습니다.",
        )
    
    db.delete(campaign)
    db.commit()
    return {"message": "캠페인이 삭제되었습니다."}

@router.post("/{campaign_id}/applications", response_model=CampaignApplicationResponse)
def create_campaign_application(
    *,
    db: Session = Depends(get_db),
    campaign_id: int,
    application_in: CampaignApplicationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    캠페인에 대한 신청을 생성합니다.
    """
    if current_user.user_type != UserType.INFLUENCER:
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 캠페인에 신청할 수 있습니다.",
        )
    
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="캠페인을 찾을 수 없습니다.",
        )
    
    if campaign.status != CampaignStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail="활성화된 캠페인에만 신청할 수 있습니다.",
        )
    
    if campaign.current_applications >= campaign.max_applications:
        raise HTTPException(
            status_code=400,
            detail="신청 가능한 인원이 초과되었습니다.",
        )
    
    existing_application = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id == campaign_id,
        CampaignApplication.influencer_id == current_user.id
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="이미 신청한 캠페인입니다.",
        )
    
    application = CampaignApplication(
        **application_in.dict(),
        influencer_id=current_user.id,
        status="pending"
    )
    db.add(application)
    campaign.current_applications += 1
    db.commit()
    db.refresh(application)
    return application

@router.get("/{campaign_id}/applications", response_model=CampaignApplicationList)
def read_campaign_applications(
    campaign_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    캠페인의 신청 목록을 조회합니다.
    """
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="캠페인을 찾을 수 없습니다.",
        )
    
    if campaign.brand_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="해당 캠페인의 신청 목록을 조회할 권한이 없습니다.",
        )
    
    applications = db.query(CampaignApplication).filter(
        CampaignApplication.campaign_id == campaign_id
    ).all()
    
    return {
        "total": len(applications),
        "items": applications
    }

@router.put("/applications/{application_id}", response_model=CampaignApplicationResponse)
def update_campaign_application(
    *,
    db: Session = Depends(get_db),
    application_id: int,
    application_in: CampaignApplicationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    캠페인 신청의 상태를 수정합니다.
    """
    application = db.query(CampaignApplication).filter(
        CampaignApplication.id == application_id
    ).first()
    if not application:
        raise HTTPException(
            status_code=404,
            detail="신청을 찾을 수 없습니다.",
        )
    
    campaign = application.campaign
    if campaign.brand_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="해당 신청을 수정할 권한이 없습니다.",
        )
    
    update_data = application_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)
    
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/me", response_model=List[schemas.Campaign])
def read_campaigns_me(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """
    현재 로그인한 사용자의 캠페인 목록을 조회합니다.
    """
    campaigns = crud.campaign.get_by_user_id(db, user_id=current_user.user_id)
    return campaigns

@router.get("/me/applications", response_model=List[schemas.CampaignApplication])
def read_my_applications(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """
    현재 로그인한 사용자의 캠페인 신청 목록을 조회합니다.
    """
    applications = crud.campaign_application.get_by_user_id(db, user_id=current_user.user_id)
    return applications 