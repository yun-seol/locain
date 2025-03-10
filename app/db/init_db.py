import os
import sqlite3
from pathlib import Path

def init_db():
    # 데이터베이스 파일 경로
    db_path = Path(__file__).parent / "test.db"
    
    # 기존 데이터베이스 파일이 있다면 삭제
    if db_path.exists():
        os.remove(db_path)
    
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 스키마 파일 읽기
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()
    
    # 스키마 실행
    cursor.executescript(schema)
    
    # 시드 데이터 파일 읽기
    seed_path = Path(__file__).parent / "seed.sql"
    with open(seed_path, "r", encoding="utf-8") as f:
        seed = f.read()
    
    # 시드 데이터 실행
    cursor.executescript(seed)
    
    # 변경사항 저장 및 연결 종료
    conn.commit()
    conn.close()
    
    print("데이터베이스 초기화가 완료되었습니다.")

if __name__ == "__main__":
    init_db() 