from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserType
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: CategoryCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    새로운 카테고리를 생성합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    category = Category(**category_in.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    카테고리 목록을 조회합니다.
    """
    categories = db.query(Category).filter(Category.is_active == True).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    특정 카테고리를 조회합니다.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: CategoryUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    카테고리를 수정합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    
    for field, value in category_in.dict(exclude_unset=True).items():
        setattr(category, field, value)
    
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    카테고리를 삭제합니다. (관리자 전용)
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    
    category.is_active = False
    db.add(category)
    db.commit()
    return {"message": "카테고리가 삭제되었습니다."} 