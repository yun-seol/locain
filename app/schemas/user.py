from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.models.user import UserType

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserType
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    user_id: int
    created_at: date
    updated_at: Optional[date] = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

class UserList(BaseModel):
    total: int
    items: List[UserResponse]

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str

    class Config:
        from_attributes = True 