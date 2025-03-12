from typing import Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    """카테고리 기본 스키마"""
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    """카테고리 생성 스키마"""
    pass

class CategoryUpdate(CategoryBase):
    """카테고리 수정 스키마"""
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    """카테고리 응답 스키마"""
    id: int
    
    class Config:
        from_attributes = True 