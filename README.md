# PandaRank API

인플루언서 분석 및 체험단 관리 플랫폼 API

## 기능

- 사용자 관리 (판매자/인플루언서)
- 소셜 미디어 채널 분석
- 체험단 캠페인 관리
- 포스트 분석 및 진단
- 결제 및 포인트 시스템
- SSO 로그인 지원

## 기술 스택

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- OAuth2 (SSO)

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yourusername/pandarank-api.git
cd pandarank-api
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 수정하여 필요한 설정을 입력
```

5. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

6. 서버 실행
```bash
uvicorn app.main:app --reload
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 배포

### Docker 사용

```bash
docker build -t pandarank-api .
docker run -p 8000:8000 pandarank-api
```

### 서버 배포

1. 서버에 Git 설치
2. 프로젝트 클론
3. 환경 설정
4. 서비스 실행

```bash
# 서비스 파일 생성
sudo nano /etc/systemd/system/pandarank.service

[Unit]
Description=PandaRank API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/pandarank
Environment="PATH=/path/to/pandarank/venv/bin"
ExecStart=/path/to/pandarank/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target

# 서비스 시작
sudo systemctl start pandarank
sudo systemctl enable pandarank
```

## 라이선스

MIT License 