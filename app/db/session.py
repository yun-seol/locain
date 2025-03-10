from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# 테스트 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(__file__).parent}/test.db"

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 