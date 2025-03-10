from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse
)
from app.db.database import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=UserProfileResponse)
def create_user_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: UserProfileCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    사용자 프로필을 생성합니다.
    """
    try:
        # 기존 프로필 확인
        existing_profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.id
        ).first()
        
        if existing_profile:
            raise HTTPException(
                status_code=400,
                detail="이미 프로필이 존재합니다.",
            )
        
        # 프로필 생성
        profile = UserProfile(
            **profile_in.dict(),
            user_id=current_user.id
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        return profile
        
    except Exception as e:
        logger.error(f"Profile creation failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="프로필 생성 중 오류가 발생했습니다.",
        )

@router.get("/me", response_model=UserProfileResponse)
def read_user_profile(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    현재 사용자의 프로필을 조회합니다.
    """
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="프로필을 찾을 수 없습니다.",
        )
    
    return profile

@router.put("/me", response_model=UserProfileResponse)
def update_user_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: UserProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    현재 사용자의 프로필을 업데이트합니다.
    """
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="프로필을 찾을 수 없습니다.",
            )
        
        # 프로필 업데이트
        for field, value in profile_in.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        return profile
        
    except Exception as e:
        logger.error(f"Profile update failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="프로필 업데이트 중 오류가 발생했습니다.",
        )

@router.delete("/me")
def delete_user_profile(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    현재 사용자의 프로필을 삭제합니다.
    """
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="프로필을 찾을 수 없습니다.",
            )
        
        db.delete(profile)
        db.commit()
        
        return {"message": "프로필이 성공적으로 삭제되었습니다."}
        
    except Exception as e:
        logger.error(f"Profile deletion failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="프로필 삭제 중 오류가 발생했습니다.",
        ) 