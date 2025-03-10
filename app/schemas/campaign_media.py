from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class MediaType(str, Enum):
    BLOG = "blog"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    CLIP = "clip"
    REGIONAL = "regional"

class BlogCampaignRequirements(BaseModel):
    required_posts: int = Field(default=1, description="필수 포스팅 수")
    required_words: Optional[int] = Field(None, description="필수 글자 수")
    required_images: Optional[int] = Field(None, description="필수 이미지 수")
    required_hashtags: List[str] = Field(default=[], description="필수 해시태그")
    required_links: List[str] = Field(default=[], description="필수 링크")
    required_sections: List[str] = Field(default=[], description="필수 섹션")
    required_mentions: List[str] = Field(default=[], description="필수 멘션")
    required_embed_codes: List[str] = Field(default=[], description="필수 임베드 코드")

class InstagramCampaignRequirements(BaseModel):
    required_posts: int = Field(default=1, description="필수 포스팅 수")
    required_stories: Optional[int] = Field(None, description="필수 스토리 수")
    required_reels: Optional[int] = Field(None, description="필수 릴스 수")
    required_hashtags: List[str] = Field(default=[], description="필수 해시태그")
    required_mentions: List[str] = Field(default=[], description="필수 멘션")
    required_links: List[str] = Field(default=[], description="필수 링크")
    required_highlights: Optional[List[str]] = Field(None, description="필수 하이라이트")

class YoutubeCampaignRequirements(BaseModel):
    required_videos: int = Field(default=1, description="필수 영상 수")
    required_duration: Optional[int] = Field(None, description="필수 영상 길이(초)")
    required_thumbnail: bool = Field(default=True, description="썸네일 필수 여부")
    required_description: bool = Field(default=True, description="설명 필수 여부")
    required_hashtags: List[str] = Field(default=[], description="필수 해시태그")
    required_links: List[str] = Field(default=[], description="필수 링크")
    required_mentions: List[str] = Field(default=[], description="필수 멘션")

class ClipCampaignRequirements(BaseModel):
    required_clips: int = Field(default=1, description="필수 클립 수")
    required_duration: Optional[int] = Field(None, description="필수 클립 길이(초)")
    required_hashtags: List[str] = Field(default=[], description="필수 해시태그")
    required_mentions: List[str] = Field(default=[], description="필수 멘션")
    required_links: List[str] = Field(default=[], description="필수 링크")

class RegionalCampaignRequirements(BaseModel):
    required_region: str = Field(..., description="필수 지역")
    required_visits: int = Field(default=1, description="필수 방문 횟수")
    required_posts: int = Field(default=1, description="필수 포스팅 수")
    required_images: Optional[int] = Field(None, description="필수 이미지 수")
    required_hashtags: List[str] = Field(default=[], description="필수 해시태그")
    required_mentions: List[str] = Field(default=[], description="필수 멘션")
    required_links: List[str] = Field(default=[], description="필수 링크")

class CampaignMediaBase(BaseModel):
    media_type: MediaType
    campaign_id: int
    requirements: Dict[str, Any]
    additional_notes: Optional[str] = None
    required_platforms: List[str] = Field(default=[], description="필수 플랫폼")
    required_audience: Optional[int] = Field(None, description="필수 구독자 수")
    required_engagement: Optional[float] = Field(None, description="필수 참여율")
    required_followers: Optional[int] = Field(None, description="필수 팔로워 수")

class CampaignMediaCreate(CampaignMediaBase):
    pass

class CampaignMediaUpdate(CampaignMediaBase):
    pass

class CampaignMediaResponse(CampaignMediaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 