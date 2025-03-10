from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.models.user import User, UserType
from app.models.social_channel import SocialChannel
from app.schemas.social_channel import (
    SocialChannelCreate,
    SocialChannelUpdate,
    SocialChannelResponse,
    SocialChannelList,
    SocialChannelStats,
    SocialPlatform
)
from app.db.database import get_db
from datetime import datetime
from app.core.security import get_current_active_user

router = APIRouter()

@router.post("/", response_model=SocialChannelResponse)
def create_social_channel(
    *,
    db: Session = Depends(get_db),
    channel_in: SocialChannelCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    새로운 소셜 채널을 등록합니다.
    """
    if current_user.user_type != UserType.INFLUENCER:
        raise HTTPException(
            status_code=403,
            detail="인플루언서만 소셜 채널을 등록할 수 있습니다.",
        )
    
    # 이미 해당 플랫폼의 채널이 등록되어 있는지 확인
    existing_channel = db.query(SocialChannel).filter(
        SocialChannel.influencer_id == current_user.id,
        SocialChannel.platform == channel_in.platform
    ).first()
    
    if existing_channel:
        raise HTTPException(
            status_code=400,
            detail=f"이미 {channel_in.platform} 채널이 등록되어 있습니다.",
        )
    
    channel = SocialChannel(
        **channel_in.dict(),
        influencer_id=current_user.id
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.get("/", response_model=SocialChannelList)
def read_social_channels(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    platform: Optional[SocialPlatform] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    소셜 채널 목록을 조회합니다.
    """
    query = db.query(SocialChannel)
    
    if current_user.user_type == UserType.INFLUENCER:
        query = query.filter(SocialChannel.influencer_id == current_user.id)
    
    if platform:
        query = query.filter(SocialChannel.platform == platform)
    
    total = query.count()
    channels = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": channels
    }

@router.get("/{channel_id}", response_model=SocialChannelResponse)
def read_social_channel(
    channel_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 소셜 채널의 정보를 조회합니다.
    """
    channel = db.query(SocialChannel).filter(SocialChannel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=404,
            detail="소셜 채널을 찾을 수 없습니다.",
        )
    
    if current_user.user_type == UserType.INFLUENCER and channel.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 소셜 채널에 대한 접근 권한이 없습니다.",
        )
    
    return channel

@router.put("/{channel_id}", response_model=SocialChannelResponse)
def update_social_channel(
    *,
    db: Session = Depends(get_db),
    channel_id: int,
    channel_in: SocialChannelUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 소셜 채널의 정보를 수정합니다.
    """
    channel = db.query(SocialChannel).filter(SocialChannel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=404,
            detail="소셜 채널을 찾을 수 없습니다.",
        )
    
    if channel.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 소셜 채널을 수정할 권한이 없습니다.",
        )
    
    update_data = channel_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(channel, field, value)
    
    channel.updated_at = datetime.now()
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel

@router.delete("/{channel_id}")
def delete_social_channel(
    *,
    db: Session = Depends(get_db),
    channel_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    특정 소셜 채널을 삭제합니다.
    """
    channel = db.query(SocialChannel).filter(SocialChannel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=404,
            detail="소셜 채널을 찾을 수 없습니다.",
        )
    
    if channel.influencer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="해당 소셜 채널을 삭제할 권한이 없습니다.",
        )
    
    db.delete(channel)
    db.commit()
    return {"message": "소셜 채널이 삭제되었습니다."}

@router.get("/{channel_id}/stats", response_model=SocialChannelStats)
def get_channel_stats(
    channel_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 소셜 채널의 통계 정보를 조회합니다.
    """
    channel = db.query(SocialChannel).filter(SocialChannel.id == channel_id).first()
    if not channel:
        raise HTTPException(
            status_code=404,
            detail="소셜 채널을 찾을 수 없습니다.",
        )
    
    if channel.influencer_id != current_user.id and current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="해당 소셜 채널의 통계 정보를 조회할 권한이 없습니다.",
        )
    
    # TODO: 실제 통계 데이터 계산 로직 구현
    stats = SocialChannelStats(
        platform=channel.platform,
        total_followers=channel.followers_count,
        total_views=channel.average_views,
        total_likes=channel.average_likes,
        total_comments=channel.average_comments,
        total_shares=channel.average_shares,
        average_engagement_rate=channel.engagement_rate,
        last_updated=channel.updated_at
    )
    
    return stats

@router.get("/me", response_model=List[schemas.SocialChannel])
def read_social_channels_me(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """
    현재 로그인한 사용자의 소셜 채널 목록을 조회합니다.
    """
    channels = crud.social_channel.get_by_user_id(db, user_id=current_user.user_id)
    return channels

@router.get("/{channel_id}/rankings", response_model=List[schemas.BlogPostRanking])
def read_blog_post_rankings(
    channel_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    """
    특정 소셜 채널의 블로그 포스트 순위 목록을 조회합니다.
    """
    rankings = crud.blog_post_ranking.get_by_channel_id(db, channel_id=channel_id)
    return rankings

@router.post("/{channel_id}/rankings", response_model=schemas.BlogPostRanking)
def create_blog_post_ranking(
    *,
    db: Session = Depends(deps.get_db),
    channel_id: int,
    ranking_in: schemas.BlogPostRankingCreate,
    current_user: schemas.User = Depends(get_current_active_user),
):
    """
    특정 소셜 채널의 새로운 블로그 포스트 순위를 생성합니다.
    """
    channel = crud.social_channel.get(db, id=channel_id)
    if not channel:
        raise HTTPException(
            status_code=404,
            detail="소셜 채널을 찾을 수 없습니다.",
        )
    ranking = crud.blog_post_ranking.create(db, obj_in=ranking_in)
    return ranking

@router.put("/{channel_id}/rankings/{ranking_id}", response_model=schemas.BlogPostRanking)
def update_blog_post_ranking(
    *,
    db: Session = Depends(deps.get_db),
    channel_id: int,
    ranking_id: int,
    ranking_in: schemas.BlogPostRankingUpdate,
    current_user: schemas.User = Depends(get_current_active_user),
):
    """
    특정 블로그 포스트 순위의 정보를 수정합니다.
    """
    ranking = crud.blog_post_ranking.get(db, id=ranking_id)
    if not ranking:
        raise HTTPException(
            status_code=404,
            detail="블로그 포스트 순위를 찾을 수 없습니다.",
        )
    ranking = crud.blog_post_ranking.update(db, db_obj=ranking, obj_in=ranking_in)
    return ranking 