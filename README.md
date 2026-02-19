# 골연령 검사 리포트 백엔드 API

Python Flask 기반의 골연령 검사 시스템 백엔드입니다.

## 📋 프로젝트 구조

```
backend/
├── run.py                      # 서버 실행 파일
├── requirements.txt            # 패키지 의존성
├── .env.example               # 환경변수 예제
├── .gitignore                 # Git 무시 파일
├── setup.sql                  # 데이터베이스 초기화 스크립트
│
└── app/
    ├── __init__.py            # Flask 앱 팩토리
    ├── main.py                # 라우터 등록
    │
    ├── config/
    │  └── settings.py         # 데이터베이스 및 환경 설정
    │
    ├── db/
    │  ├── database.py         # MySQL 연결 및 쿼리 실행
    │  └── models.py           # 테이블 모델 및 SQL 쿼리
    │
    ├── routes/
    │  ├── __init__.py
    │  └── report.py           # API 엔드포인트
    │
    ├── services/
    │  └── report_service.py   # 비즈니스 로직
    │
    └── schemas/
       └── report_schema.py    # 응답 데이터 구조
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 설정

```bash
# MySQL 데이터베이스 및 테이블 생성
mysql -u root -p < setup.sql
```

### 3. 환경변수 설정

`.env.example` 파일을 `.env`로 복사하고 MySQL 설정을 수정하세요:

```bash
cp .env.example .env
```

`.env` 파일 수정:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=bone_report
```

### 4. 서버 실행

```bash
python run.py
```

서버는 `http://localhost:5000`에서 실행됩니다.

## 📚 API 엔드포인트

### 1. 헬스 체크
```
GET /api/reports/health
```

### 2. 환자의 최신 보고서 조회
```
GET /api/reports/patient/{patient_code}
```

**요청 예:**
```bash
curl http://localhost:5000/api/reports/patient/2024-001234
```

**응답:**
```json
{
  "success": true,
  "message": "Report retrieved successfully",
  "data": {
    "patient": {
      "id": 1,
      "patient_code": "2024-001234",
      "name": "홍길동",
      "gender": "M",
      "birth_date": "2012-05-15"
    },
    "report": {
      "report_id": 1,
      "exam_date": "2024-11-20",
      "requested_doctor": "김영희",
      "status": "completed"
    },
    "bone_age": {
      "chronological_age": "11세 9개월",
      "bone_age": "13세 5개월",
      "age_difference": "1세 8개월",
      "current_height": 107.8,
      "predicted_height_ai": 123.2
    },
    "genetic_info": {
      "father_height": 170.0,
      "mother_height": 160.0,
      "predicted_height_genetic": 171.5
    },
    "height_percentile": {
      "percentile": 1,
      "percentile_rank": "상위 99%",
      "assessment": "저신장"
    },
    "weight_info": {
      "weight": 22.5,
      "percentile": 1,
      "bmi": 17.21,
      "bmi_category": "저체중"
    },
    "xray": {
      "image_path": "/static/image/xray_001.jpg",
      "analysis_result": "좌측 손 엑스레이 분석 완료",
      "confidence_score": 0.95
    }
  }
}
```

### 3. 환자의 검사 이력 조회
```
GET /api/reports/patient/{patient_id}/history
```

### 4. 모든 환자 목록 조회 (페이징 지원)
```
GET /api/reports/patients?page=1&per_page=20
```

### 5. 환자 검색
```
GET /api/reports/patients/search?keyword=홍길동
```

## 🔧 기술 스택

- **프레임워크**: Flask 2.3.2
- **데이터베이스**: MySQL 8.0+
- **ORM**: PyMySQL (Raw SQL)
- **기타**: Flask-CORS, python-dotenv

## 💾 데이터베이스 스키마

### patients (환자)
- `id`: 기본 키
- `patient_code`: 환자 코드 (고유값)
- `name`: 환자 이름
- `gender`: 성별 (M/F)
- `birth_date`: 생년월일

### reports (검사 보고서)
- `id`: 기본 키
- `patient_id`: 환자 ID (외래키)
- `exam_date`: 검사 일자
- `requested_doctor`: 의뢰 의사
- `status`: 검사 상태 (pending/in_progress/completed/failed)

### bone_ages (골연령)
- `chronological_age`: 실제 나이
- `bone_age`: 골연령
- `age_difference`: 나이 차이
- `current_height`: 현재 키
- `predicted_height_ai`: AI 기반 예측 키

### genetic_info (유전 정보)
- `father_height`: 아버지 키
- `mother_height`: 어머니 키
- `predicted_height_genetic`: 유전적 예측 키

### height_percentiles (키 백분위)
- `percentile`: 백분위 순위
- `percentile_rank`: 상위/하위 퍼센트
- `assessment`: 저신장/정상/고신장

### weight_info (체중 정보)
- `weight`: 체중
- `percentile`: 백분위 순위
- `bmi`: 체질량 지수
- `bmi_category`: 저체중/정상/과체중/비만

### xray_analysis (엑스레이 분석)
- `image_path`: 이미지 경로
- `analysis_result`: 분석 결과
- `confidence_score`: 신뢰도 점수

## 🛠️ 주요 특징

✅ **모듈화된 구조**: config, db, routes, services, schemas 분리
✅ **데이터베이스 추상화**: Database 클래스를 통한 쿼리 실행
✅ **에러 처리**: 전역 에러 핸들러 및 예외 처리
✅ **CORS 설정**: 프론트엔드 연동 지원
✅ **환경변수 관리**: .env 파일 지원
✅ **샘플 데이터**: setup.sql에 테스트 데이터 포함

## 🔌 프론트엔드 연동

정적 파일(HTML, CSS, JS)을 제공하려면 `run.py`에 정적 파일 경로를 추가하세요:

```python
app = Flask(__name__, 
    static_folder='../static', 
    template_folder='../template'
)
```

## 📝 개발 팁

### 새로운 API 엔드포인트 추가

1. **routes/report.py**에 새로운 라우트 함수 추가
2. **services/report_service.py**에 비즈니스 로직 구현
3. **schemas/report_schema.py**에 응답 스키마 정의

### 새로운 테이블 추가

1. **setup.sql**에 CREATE TABLE 추가
2. **db/models.py**에 모델 클래스 및 쿼리 정의
3. **services/**에 서비스 함수 구현

## 🐛 문제 해결

### MySQL 연결 오류
- MySQL 서버가 실행 중인지 확인
- `.env` 파일의 MySQL 설정 확인

### 패키지 설치 오류
- Python 버전 3.8 이상 확인
- 가상 환경 재생성: `rm -rf venv` → `python -m venv venv`

## 📄 라이선스

MIT License

## 🤝 기여

버그 리포트 및 기능 요청은 이슈를 통해 제출해주세요.

## 📞 지원

질문이나 지원이 필요하면 연락주세요.
