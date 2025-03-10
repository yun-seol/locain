from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "PandaRank API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # JWT 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://apilocain:%40Yunseol2002@211.224.176.202:3306/apilocain")
    
    # SSO 설정
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    NAVER_CLIENT_ID: Optional[str] = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET: Optional[str] = os.getenv("NAVER_CLIENT_SECRET")
    KAKAO_CLIENT_ID: Optional[str] = os.getenv("KAKAO_CLIENT_ID")
    KAKAO_CLIENT_SECRET: Optional[str] = os.getenv("KAKAO_CLIENT_SECRET")

    class Config:
        case_sensitive = True

settings = Settings()

# 데이터베이스 엔진 생성
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 