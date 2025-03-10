from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class HashtagBase(BaseModel):
    name: str = Field(..., description="해시태그 이름")
    category: Optional[str] = Field(None, description="해시태그 카테고리")
    description: Optional[str] = Field(None, description="해시태그 설명")

class HashtagCreate(HashtagBase):
    pass

class HashtagUpdate(HashtagBase):
    pass

class HashtagResponse(HashtagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    usage_count: int = Field(default=0, description="사용 횟수")

    class Config:
        from_attributes = True

class HashtagList(BaseModel):
    hashtags: List[HashtagResponse]
    total: int
    page: int
    size: int 