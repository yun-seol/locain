from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class UserProfileBase(BaseModel):
    self_introduction: Optional[str] = Field(None, description="자기소개")
    interests: List[str] = Field(default=[], description="관심사")
    main_activity_areas: List[str] = Field(default=[], description="주 활동 지역")
    camera_type: Optional[str] = Field(None, description="사용 카메라 종류")
    face_exposure: bool = Field(default=False, description="얼굴 노출 가능 여부")
    is_shared_blog: bool = Field(default=False, description="공동 블로그 운영 여부")

class UserSizeInfo(BaseModel):
    top_size: Optional[str] = Field(None, description="상의 사이즈")
    bottom_size: Optional[str] = Field(None, description="하의 사이즈")
    shoe_size: Optional[int] = Field(None, description="신발 사이즈")
    height: Optional[str] = Field(None, description="키")
    skin_type: Optional[str] = Field(None, description="피부 타입")

class UserLifeInfo(BaseModel):
    marital_status: Optional[str] = Field(None, description="결혼 여부")
    has_children: bool = Field(default=False, description="자녀 유무")
    children_info: List[str] = Field(default=[], description="자녀 정보")
    occupation: Optional[str] = Field(None, description="직업")
    has_pets: bool = Field(default=False, description="반려동물 유무")
    pet_types: List[str] = Field(default=[], description="반려동물 종류")

class UserProfileCreate(UserProfileBase):
    size_info: Optional[UserSizeInfo] = None
    life_info: Optional[UserLifeInfo] = None

class UserProfileUpdate(UserProfileCreate):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    size_info: Optional[UserSizeInfo] = None
    life_info: Optional[UserLifeInfo] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 