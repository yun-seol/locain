from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from app.models.review import ReviewStatus

class ReviewContentBase(BaseModel):
    content: str
    rating: int
    hashtags: List[str] = []
    images: List[str] = []
    platform: str
    post_url: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    status: ReviewStatus = ReviewStatus.PENDING
    brand_feedback: Optional[str] = None
    brand_rating: Optional[int] = None
    brand_comment: Optional[str] = None

class ReviewContentCreate(ReviewContentBase):
    campaign_application_id: int
    influencer_id: int

class ReviewContentUpdate(ReviewContentBase):
    pass

class ReviewContent(ReviewContentBase):
    id: int
    campaign_application_id: int
    influencer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewContentResponse(ReviewContentBase):
    id: int
    influencer_id: int
    status: ReviewStatus
    created_at: datetime
    updated_at: datetime
    brand_feedback: Optional[str] = None
    brand_rating: Optional[int] = Field(None, ge=1, le=5)
    brand_comment: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewContentInDB(ReviewContentResponse):
    pass

class ReviewContentList(BaseModel):
    total: int
    items: List[ReviewContentResponse]

    class Config:
        from_attributes = True

class ReviewImageBase(BaseModel):
    image_url: str
    caption: Optional[str] = None
    order: int = 0

class ReviewImageCreate(ReviewImageBase):
    review_content_id: int

class ReviewImageUpdate(ReviewImageBase):
    pass

class ReviewImage(ReviewImageBase):
    id: int
    review_content_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewImageResponse(ReviewImageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewImageList(BaseModel):
    total: int
    items: List[ReviewImageResponse]

    class Config:
        from_attributes = True

class ReviewStats(BaseModel):
    total_reviews: int
    average_rating: float
    total_views: int
    total_likes: int
    total_comments: int
    total_shares: int
    average_engagement_rate: float
    last_updated: datetime

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    campaign_id: int
    user_id: int
    rating: int
    content: str
    is_public: bool = True

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = None

class ReviewResponse(ReviewBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True 