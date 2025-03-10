from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.security import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.InfluencerResponse)
def create_influencer(
    *,
    db: Session = Depends(deps.get_db),
    influencer_in: schemas.InfluencerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    새로운 인플루언서 정보를 생성합니다.
    """
    if current_user.role != "influencer":
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 프로필을 생성할 수 있습니다.",
        )
    
    influencer = crud.influencer.get_by_user_id(db, user_id=current_user.id)
    if influencer:
        raise HTTPException(
            status_code=400,
            detail="이미 인플루언서 프로필이 존재합니다.",
        )
    
    influencer_in.user_id = current_user.id
    influencer = crud.influencer.create(db, obj_in=influencer_in)
    return influencer

@router.get("/", response_model=List[schemas.InfluencerResponse])
def read_influencers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    인플루언서 목록을 조회합니다.
    """
    influencers = crud.influencer.get_multi(db, skip=skip, limit=limit)
    return influencers

@router.get("/me", response_model=schemas.InfluencerResponse)
def read_influencer_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    현재 로그인한 인플루언서의 프로필을 조회합니다.
    """
    if current_user.role != "influencer":
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 프로필을 조회할 수 있습니다.",
        )
    
    influencer = crud.influencer.get_by_user_id(db, user_id=current_user.id)
    if not influencer:
        raise HTTPException(
            status_code=404,
            detail="인플루언서 프로필이 존재하지 않습니다.",
        )
    return influencer

@router.put("/me", response_model=schemas.InfluencerResponse)
def update_influencer_me(
    *,
    db: Session = Depends(deps.get_db),
    influencer_in: schemas.InfluencerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    현재 로그인한 인플루언서의 프로필을 업데이트합니다.
    """
    if current_user.role != "influencer":
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 프로필을 업데이트할 수 있습니다.",
        )
    
    influencer = crud.influencer.get_by_user_id(db, user_id=current_user.id)
    if not influencer:
        raise HTTPException(
            status_code=404,
            detail="인플루언서 프로필이 존재하지 않습니다.",
        )
    
    influencer = crud.influencer.update(db, db_obj=influencer, obj_in=influencer_in)
    return influencer

@router.delete("/me")
def delete_influencer_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    현재 로그인한 인플루언서의 프로필을 삭제합니다.
    """
    if current_user.role != "influencer":
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 프로필을 삭제할 수 있습니다.",
        )
    
    influencer = crud.influencer.get_by_user_id(db, user_id=current_user.id)
    if not influencer:
        raise HTTPException(
            status_code=404,
            detail="인플루언서 프로필이 존재하지 않습니다.",
        )
    
    influencer = crud.influencer.remove(db, id=influencer.id)
    return {"ok": True}

@router.get("/search", response_model=List[schemas.InfluencerResponse])
def search_influencers(
    *,
    db: Session = Depends(deps.get_db),
    categories: List[str] = Query(None),
    regions: List[str] = Query(None),
    min_followers: int = Query(None),
    max_followers: int = Query(None),
    min_engagement_rate: float = Query(None),
    max_engagement_rate: float = Query(None),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    조건에 맞는 인플루언서를 검색합니다.
    """
    filters = {}
    if categories:
        filters["categories"] = categories
    if regions:
        filters["preferred_regions"] = regions
    if min_followers is not None:
        filters["min_followers"] = min_followers
    if max_followers is not None:
        filters["max_followers"] = max_followers
    if min_engagement_rate is not None:
        filters["min_engagement_rate"] = min_engagement_rate
    if max_engagement_rate is not None:
        filters["max_engagement_rate"] = max_engagement_rate
    
    influencers = crud.influencer.get_multi_by_filters(
        db, filters=filters, skip=skip, limit=limit
    )
    return influencers

@router.get("/{influencer_id}", response_model=schemas.InfluencerResponse)
def read_influencer(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 인플루언서의 프로필을 조회합니다.
    """
    influencer = crud.influencer.get(db, id=influencer_id)
    if not influencer:
        raise HTTPException(
            status_code=404,
            detail="인플루언서 프로필이 존재하지 않습니다.",
        )
    return influencer

# 인플루언서 통계 관련 엔드포인트
@router.get("/{influencer_id}/stats", response_model=schemas.InfluencerStats)
def read_influencer_stats(
    influencer_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """
    특정 인플루언서의 통계 정보를 조회합니다.
    """
    stats = crud.influencer_stats.get_by_influencer_id(db, influencer_id=influencer_id)
    if not stats:
        raise HTTPException(
            status_code=404,
            detail="통계 정보를 찾을 수 없습니다.",
        )
    return stats

@router.put("/{influencer_id}/stats", response_model=schemas.InfluencerStats)
def update_influencer_stats(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    stats_in: schemas.InfluencerStatsUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    특정 인플루언서의 통계 정보를 수정합니다.
    """
    stats = crud.influencer_stats.get_by_influencer_id(db, influencer_id=influencer_id)
    if not stats:
        raise HTTPException(
            status_code=404,
            detail="통계 정보를 찾을 수 없습니다.",
        )
    stats = crud.influencer_stats.update(db, db_obj=stats, obj_in=stats_in)
    return stats

# 인플루언서 플랫폼 관련 엔드포인트
@router.get("/{influencer_id}/platforms", response_model=List[schemas.InfluencerPlatform])
def read_influencer_platforms(
    influencer_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """
    특정 인플루언서의 플랫폼 정보를 조회합니다.
    """
    platforms = crud.influencer_platform.get_by_influencer_id(db, influencer_id=influencer_id)
    return platforms

@router.post("/{influencer_id}/platforms", response_model=schemas.InfluencerPlatform)
def create_influencer_platform(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    platform_in: schemas.InfluencerPlatformCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    특정 인플루언서의 새로운 플랫폼 정보를 생성합니다.
    """
    platform = crud.influencer_platform.create(db, obj_in=platform_in)
    return platform

@router.put("/{influencer_id}/platforms/{platform_id}", response_model=schemas.InfluencerPlatform)
def update_influencer_platform(
    *,
    db: Session = Depends(deps.get_db),
    influencer_id: int,
    platform_id: int,
    platform_in: schemas.InfluencerPlatformUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    특정 인플루언서의 플랫폼 정보를 수정합니다.
    """
    platform = crud.influencer_platform.get(db, id=platform_id)
    if not platform:
        raise HTTPException(
            status_code=404,
            detail="플랫폼 정보를 찾을 수 없습니다.",
        )
    platform = crud.influencer_platform.update(db, db_obj=platform, obj_in=platform_in)
    return platform 