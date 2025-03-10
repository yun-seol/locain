import pytest
from fastapi.testclient import TestClient
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate

def test_create_user(client: TestClient):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
        "role": "user"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["role"] == user_data["role"]
    assert "password" not in data

def test_read_users(client: TestClient, db: Session):
    # 테스트 사용자 생성
    user = User(
        email="test@example.com",
        password="hashed_password",
        full_name="Test User",
        role="user"
    )
    db.add(user)
    db.commit()
    
    # 관리자 토큰 생성
    admin_token = create_access_token(subject=1, role="admin")
    
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_user_me(client: TestClient, db: Session):
    # 테스트 사용자 생성
    user = User(
        email="test@example.com",
        password="hashed_password",
        full_name="Test User",
        role="user"
    )
    db.add(user)
    db.commit()
    
    # 사용자 토큰 생성
    user_token = create_access_token(subject=user.id, role="user")
    
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["full_name"] == user.full_name

def test_update_user_me(client: TestClient, db: Session):
    # 테스트 사용자 생성
    user = User(
        email="test@example.com",
        password="hashed_password",
        full_name="Test User",
        role="user"
    )
    db.add(user)
    db.commit()
    
    # 사용자 토큰 생성
    user_token = create_access_token(subject=user.id, role="user")
    
    update_data = {
        "full_name": "Updated Name"
    }
    
    response = client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]

def test_delete_user(client: TestClient, db: Session):
    # 테스트 사용자 생성
    user = User(
        email="test@example.com",
        password="hashed_password",
        full_name="Test User",
        role="user"
    )
    db.add(user)
    db.commit()
    
    # 관리자 토큰 생성
    admin_token = create_access_token(subject=1, role="admin")
    
    response = client.delete(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # 삭제 확인
    deleted_user = db.query(User).filter(User.id == user.id).first()
    assert deleted_user is None 