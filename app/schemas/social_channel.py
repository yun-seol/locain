from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class SocialPlatform(str, Enum):
    KAKAO = "kakao"
    NAVER = "naver"
    GOOGLE = "google"
    APPLE = "apple"

class SocialChannelBase(BaseModel):
    platform: SocialPlatform
    channel_name: str
    channel_url: str
    followers_count: int = 0
    average_views: int = 0
    average_likes: int = 0
    average_comments: int = 0
    average_shares: int = 0
    engagement_rate: float = 0.0
    is_active: bool = True
    followers: int
    posts: int

class SocialChannelCreate(SocialChannelBase):
    user_id: int

class SocialChannelUpdate(SocialChannelBase):
    pass

class SocialChannelResponse(SocialChannelBase):
    id: int
    influencer_id: int
    created_at: date
    updated_at: date
    last_sync_at: Optional[datetime] = None
    platform_specific_data: Optional[dict] = None

    class Config:
        from_attributes = True

class SocialChannelInDB(SocialChannelResponse):
    pass

class SocialChannelList(BaseModel):
    total: int
    items: List[SocialChannelResponse]

    class Config:
        from_attributes = True

class SocialChannelStats(BaseModel):
    platform: SocialPlatform
    total_followers: int
    total_views: int
    total_likes: int
    total_comments: int
    total_shares: int
    average_engagement_rate: float
    last_updated: datetime

    class Config:
        from_attributes = True

class BlogPostRankingBase(BaseModel):
    post_url: str
    title: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    ranking_date: datetime

class BlogPostRankingCreate(BlogPostRankingBase):
    channel_id: int

class BlogPostRankingUpdate(BaseModel):
    post_url: Optional[str] = None
    title: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    ranking_date: Optional[datetime] = None

class BlogPostRankingInDBBase(BlogPostRankingBase):
    id: int
    channel_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BlogPostRanking(BlogPostRankingInDBBase):
    pass

class BlogPostRankingInDB(BlogPostRankingInDBBase):
    pass

class SocialChannel(SocialChannelBase):
    id: int
    user_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class BlogPostRankingResponse(BlogPostRankingBase):
    id: int
    channel_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class BlogPostRankingList(BaseModel):
    total: int
    items: List[BlogPostRankingResponse]

    class Config:
        from_attributes = True

class BlogPostRankingInDB(BlogPostRanking):
    pass 