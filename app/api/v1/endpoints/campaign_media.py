from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserType
from app.models.campaign_media import CampaignMedia
from app.schemas.campaign_media import (
    CampaignMediaCreate,
    CampaignMediaUpdate,
    CampaignMediaResponse,
    MediaType
)
from app.db.database import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=CampaignMediaResponse)
def create_campaign_media(
    *,
    db: Session = Depends(get_db),
    media_in: CampaignMediaCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    매체별 체험단 요구사항을 생성합니다.
    """
    try:
        if current_user.user_type != UserType.BRAND:
            raise HTTPException(
                status_code=403,
                detail="브랜드만 체험단 요구사항을 생성할 수 있습니다.",
            )
        
        # 기존 매체 요구사항 확인
        existing_media = db.query(CampaignMedia).filter(
            CampaignMedia.campaign_id == media_in.campaign_id,
            CampaignMedia.media_type == media_in.media_type
        ).first()
        
        if existing_media:
            raise HTTPException(
                status_code=400,
                detail="이미 해당 매체의 요구사항이 존재합니다.",
            )
        
        # 매체 요구사항 생성
        media = CampaignMedia(**media_in.dict())
        db.add(media)
        db.commit()
        db.refresh(media)
        
        return media
        
    except Exception as e:
        logger.error(f"Campaign media creation failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="매체 요구사항 생성 중 오류가 발생했습니다.",
        )

@router.get("/campaign/{campaign_id}", response_model=List[CampaignMediaResponse])
def read_campaign_media(
    campaign_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    캠페인의 매체별 요구사항을 조회합니다.
    """
    media_list = db.query(CampaignMedia).filter(
        CampaignMedia.campaign_id == campaign_id
    ).all()
    
    return media_list

@router.get("/{media_id}", response_model=CampaignMediaResponse)
def read_campaign_media_detail(
    media_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 매체 요구사항의 상세 정보를 조회합니다.
    """
    media = db.query(CampaignMedia).filter(
        CampaignMedia.id == media_id
    ).first()
    
    if not media:
        raise HTTPException(
            status_code=404,
            detail="매체 요구사항을 찾을 수 없습니다.",
        )
    
    return media

@router.put("/{media_id}", response_model=CampaignMediaResponse)
def update_campaign_media(
    *,
    db: Session = Depends(get_db),
    media_id: int,
    media_in: CampaignMediaUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    매체 요구사항을 업데이트합니다.
    """
    try:
        if current_user.user_type != UserType.BRAND:
            raise HTTPException(
                status_code=403,
                detail="브랜드만 매체 요구사항을 수정할 수 있습니다.",
            )
        
        media = db.query(CampaignMedia).filter(
            CampaignMedia.id == media_id
        ).first()
        
        if not media:
            raise HTTPException(
                status_code=404,
                detail="매체 요구사항을 찾을 수 없습니다.",
            )
        
        # 매체 요구사항 업데이트
        for field, value in media_in.dict(exclude_unset=True).items():
            setattr(media, field, value)
        
        db.add(media)
        db.commit()
        db.refresh(media)
        
        return media
        
    except Exception as e:
        logger.error(f"Campaign media update failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="매체 요구사항 업데이트 중 오류가 발생했습니다.",
        )

@router.delete("/{media_id}")
def delete_campaign_media(
    media_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    매체 요구사항을 삭제합니다.
    """
    try:
        if current_user.user_type != UserType.BRAND:
            raise HTTPException(
                status_code=403,
                detail="브랜드만 매체 요구사항을 삭제할 수 있습니다.",
            )
        
        media = db.query(CampaignMedia).filter(
            CampaignMedia.id == media_id
        ).first()
        
        if not media:
            raise HTTPException(
                status_code=404,
                detail="매체 요구사항을 찾을 수 없습니다.",
            )
        
        db.delete(media)
        db.commit()
        
        return {"message": "매체 요구사항이 성공적으로 삭제되었습니다."}
        
    except Exception as e:
        logger.error(f"Campaign media deletion failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="매체 요구사항 삭제 중 오류가 발생했습니다.",
        ) 