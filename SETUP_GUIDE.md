# 홈앤쇼핑 일일 매출 현황 대시보드 - 환경설정 가이드

**작성일:** 2026-06-04  
**프로젝트:** 홈앤쇼핑 일일 매출 현황 대시보드  
**상태:** ✅ Supabase 연동 완료

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [Supabase 설정](#supabase-설정)
3. [Streamlit 설정](#streamlit-설정)
4. [데이터베이스 구조](#데이터베이스-구조)
5. [로컬 실행 방법](#로컬-실행-방법)
6. [Streamlit Cloud 배포](#streamlit-cloud-배포)
7. [파일 구조](#파일-구조)
8. [트러블슈팅](#트러블슈팅)

---

## 🎯 프로젝트 개요

### 목표
Streamlit으로 만든 대시보드를 Supabase 데이터베이스와 연동하여 실시간 주문 데이터를 시각화하는 애플리케이션.

### 주요 기능
- 📊 일별 매출 추이 차트
- 📈 카테고리별 매출 비중 (파이 차트)
- 💰 오늘/어제 매출 비교
- 📉 어제 대비 증감률

### 기술 스택
- **Frontend:** Streamlit
- **Database:** Supabase (PostgreSQL)
- **Data Visualization:** Plotly
- **Data Processing:** Pandas
- **API:** Supabase REST API

---

## 🔐 Supabase 설정

### 1. Supabase 프로젝트 정보

```
프로젝트 ID: grbbbrgrcplvfettmlyq
리전: ap-northeast-2 (서울)
상태: ACTIVE_HEALTHY
```

### 2. 테이블 생성 (orders)

**테이블명:** `orders`

**칼럼 구조:**

| 칼럼명 | 데이터 타입 | 설명 | 원본 칼럼명 |
|--------|-----------|------|-----------|
| id | BIGINT (PK) | 자동 증가 ID | - |
| order_id | TEXT | 주문 ID | 주문ID |
| order_date | DATE | 주문 날짜 | 주문일자 |
| product | TEXT | 상품명 | 상품 |
| md_user | TEXT | MD 유저 | MD유저 |
| category | TEXT | 카테고리 | 카테고리 |
| team | TEXT | 팀명 | 팀 |
| media | TEXT | 매체/채널 | 매체 |
| product_sales | INTEGER | 상품취급액 | 상품취급액 |
| additional_sales | INTEGER | 부가매출 | 부가매출 |
| service_sales | INTEGER | 서비스매출 | 서비스매출 |
| advertising_sales | INTEGER | 광고매출 | 광고매출 |
| points | INTEGER | 적립금 | 적립금 |
| discount | INTEGER | 할인금액 | 할인금액 |
| sales_cost | INTEGER | 매출원가 | 매출원가 |
| gross_profit | INTEGER | 매출총이익 | 매출총이익 |
| variable_cost | INTEGER | 변동비 | 변동비 |
| contribution_profit | INTEGER | 공헌이익 | 공헌이익 |
| created_at | TIMESTAMP | 생성 시간 | - |

**인덱스:**
- Primary Key: `id`
- Index: `order_id`, `order_date`

### 3. 데이터 삽입

**총 12개 레코드 삽입:**
- ORD001 ~ ORD012
- 날짜: 2026-06-01 ~ 2026-06-04
- 카테고리: 뷰티, 생활용품, 전자, 패션, 스포츠, 식품
- 총 매출: ₩1,985,000

### 4. API 키

**Publishable Key (Anon):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdyYmJicmdyY3BsdmZldHRtbHlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA1MzU0ODAsImV4cCI6MjA5NjExMTQ4MH0.2gOt_ueQlbtB7PXyr-g5yG0wxPLCr9W4h0oWv2ZAxMM
```

**REST API 엔드포인트:**
```
https://grbbbrgrcplvfettmlyq.supabase.co/rest/v1/orders
```

---

## 🎨 Streamlit 설정

### 1. Secrets 관리

#### 로컬 환경 (`.streamlit/secrets.toml`)

```toml
# Supabase Configuration
SUPABASE_URL = "https://grbbbrgrcplvfettmlyq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdyYmJicmdyY3BsdmZldHRtbHlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA1MzU0ODAsImV4cCI6MjA5NjExMTQ4MH0.2gOt_ueQlbtB7PXyr-g5yG0wxPLCr9W4h0oWv2ZAxMM"
```

**위치:** `c:\shlee\.streamlit\secrets.toml`

⚠️ **주의:** 이 파일은 `.gitignore`로 제외되어 git에 커밋되지 않습니다!

#### Streamlit Cloud 환경

1. Streamlit Cloud 앱 페이지 접속
2. 우상단 **⋮ (메뉴)** → **Manage app**
3. **Secrets** 탭 클릭
4. 위 TOML 내용 입력
5. **Save** 클릭

### 2. app.py 주요 코드

**Supabase 데이터 로드:**

```python
@st.cache_data(ttl=300)
def load_orders_data():
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f'{url}/rest/v1/orders?select=*', headers=headers)
    # ... 에러 처리 로직
```

**특징:**
- ✅ 5분 캐시 (ttl=300)
- ✅ secrets 없을 때 None 반환
- ✅ API 오류 시 graceful 처리
- ✅ 데이터 없을 때 안내 메시지 표시

### 3. 의존성 (requirements.txt)

```
streamlit
pandas
plotly
```

**설치 방법:**

```bash
pip install -r requirements.txt
```

---

## 💾 데이터베이스 구조

### 테이블 관계도

```
orders (메인 테이블)
├── order_id (PK 아님, 대신 id가 PK)
├── order_date (인덱스)
├── product
├── category
├── team
├── media
└── 금액 관련 칼럼들...
```

### 데이터 샘플

```json
{
  "id": 1,
  "order_id": "ORD001",
  "order_date": "2026-06-01",
  "product": "시그니처 세트A",
  "md_user": "MD001",
  "category": "뷰티",
  "team": "뷰티팀",
  "media": "CJ온스타일",
  "product_sales": 150000,
  "additional_sales": 5000,
  "service_sales": 0,
  "advertising_sales": 0,
  "points": 2000,
  "discount": 15000,
  "sales_cost": 75000,
  "gross_profit": 75000,
  "variable_cost": 8000,
  "contribution_profit": 67000,
  "created_at": "2026-06-04T07:49:05.482986+00:00"
}
```

---

## 🚀 로컬 실행 방법

### 1. 환경 준비

```bash
# 저장소 클론
git clone https://github.com/tqqq3xm-droid/test.git
cd test

# 의존성 설치
pip install -r requirements.txt
```

### 2. Secrets 설정

`.streamlit/secrets.toml` 파일 생성:

```toml
SUPABASE_URL = "https://grbbbrgrcplvfettmlyq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. 앱 실행

```bash
streamlit run app.py
```

**출력:**

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://YOUR_IP:8501
```

### 4. 브라우저 접속

```
http://localhost:8501
```

---

## ☁️ Streamlit Cloud 배포

### 1. GitHub 저장소 연결

```
Repository: https://github.com/tqqq3xm-droid/test
Branch: main
File: app.py
```

### 2. Streamlit Cloud에 배포

1. [Streamlit Cloud](https://streamlit.io/cloud) 접속
2. "New app" 클릭
3. GitHub 저장소 선택
4. Branch: `main`, File: `app.py` 선택
5. "Deploy" 클릭

### 3. Secrets 추가

배포 후 앱 설정에서:

1. **Manage app** 클릭
2. **Secrets** 탭
3. TOML 형식으로 입력:

```toml
SUPABASE_URL = "https://grbbbrgrcplvfettmlyq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

4. **Save** 클릭

### 4. 앱 재시작

자동 재시작되거나 "Rerun" 클릭

---

## 📁 파일 구조

```
c:\shlee\
├── app.py                          # Streamlit 앱 메인 파일
├── requirements.txt                # Python 의존성
├── README.md                       # 프로젝트 README
├── SETUP_GUIDE.md                  # 이 파일
├── 주문_데이터.csv                 # 원본 CSV 데이터
├── .gitignore                      # Git 제외 파일 설정
├── .env                            # 환경 변수 (git 제외)
│
├── .streamlit/
│   └── secrets.toml                # Supabase 설정 (git 제외)
│   └── config.toml                 # (옵션) 추가 설정
│
└── .git/                           # Git 저장소
```

### 주요 파일 설명

| 파일 | 목적 | git 포함 |
|------|------|---------|
| app.py | Streamlit 앱 | ✅ |
| requirements.txt | 의존성 | ✅ |
| .streamlit/secrets.toml | Supabase API 키 | ❌ |
| .env | 환경 변수 | ❌ |
| .gitignore | git 제외 설정 | ✅ |

---

## 🔄 데이터 흐름

```
CSV 파일 (주문_데이터.csv)
    ↓
Supabase (orders 테이블)
    ↓
REST API (HTTPS 요청)
    ↓
Streamlit app.py
    ↓
Streamlit secrets.toml
    ↓
대시보드 (브라우저)
```

### API 호출 흐름

```python
1. app.py 실행
2. st.secrets에서 SUPABASE_URL, SUPABASE_KEY 읽기
3. requests.get() 으로 REST API 호출
4. 응답 데이터를 DataFrame으로 변환
5. 한글 칼럼명으로 매핑
6. Plotly로 시각화
7. Streamlit으로 렌더링
```

---

## 🛠️ 트러블슈팅

### 문제 1: "Invalid API key" 오류

**증상:**
```
Supabase 연결 오류: 401
응답: {"message":"Invalid API key"}
```

**해결:**
1. ✅ SUPABASE_KEY 복사 정확성 확인
2. ✅ `.streamlit/secrets.toml` 파일 존재 확인
3. ✅ TOML 파일 포맷 확인 (쉼표, 따옴표 등)
4. ✅ Streamlit 재시작

```bash
# 로컬: secrets.toml이 있는 디렉토리에서 실행
streamlit run app.py

# 또는 secrets 경로 명시
STREAMLIT_SECRETS_PATH=.streamlit/secrets.toml streamlit run app.py
```

### 문제 2: "데이터가 없습니다" 메시지

**증상:**
- 대시보드에 "⚠️ Supabase 연결 오류" 표시
- 데이터 로드 실패

**해결:**
1. ✅ Supabase 콘솔에서 orders 테이블 확인
2. ✅ 데이터 존재 확인: `SELECT COUNT(*) FROM orders;`
3. ✅ API 엔드포인트 테스트:
   ```bash
   curl -H "apikey: YOUR_KEY" \
        "https://grbbbrgrcplvfettmlyq.supabase.co/rest/v1/orders"
   ```

### 문제 3: 로컬에서는 되는데 Streamlit Cloud에서 안 됨

**원인:** Streamlit Cloud에서 secrets이 설정되지 않음

**해결:**
1. ✅ Streamlit Cloud 앱 관리 페이지 접속
2. ✅ "Secrets" 탭에서 설정
3. ✅ TOML 형식 확인
4. ✅ "Save" 클릭 후 앱 자동 재시작

### 문제 4: 한글이 깨져서 표시됨

**원인:** 콘솔 인코딩 문제 (실제 데이터는 정상)

**해결:**
- ✅ 브라우저에서는 정상 표시됨
- ✅ 콘솔 출력은 무시해도 됨
- ✅ Streamlit 대시보드 확인

---

## 📊 모니터링

### Supabase 대시보드

```
https://supabase.com/dashboard
```

**확인 사항:**
- ✅ 테이블 데이터 확인
- ✅ API 요청 로그
- ✅ 성능 모니터링

### Streamlit 앱 모니터링

**로컬:**
```bash
streamlit run app.py --logger.level=debug
```

**Streamlit Cloud:**
- 앱 페이지의 "Manage app" → "View logs"에서 확인

---

## 🔄 업데이트 이력

### 2026-06-04

**초기 설정 완료:**
- ✅ Supabase 테이블 생성
- ✅ CSV 데이터 삽입 (12개 레코드)
- ✅ Streamlit과 Supabase 연동
- ✅ .streamlit/secrets.toml 설정
- ✅ 에러 처리 개선
- ✅ GitHub 업로드

**커밋:**
```
2ea9b02 - Connect Streamlit to Supabase with secrets.toml configuration
d3c1d3e - Improve Streamlit Cloud compatibility with better error handling
```

---

## 📚 참고 자료

### Supabase 공식 문서
- [Supabase Overview](https://supabase.com/docs)
- [REST API](https://supabase.com/docs/guides/api)
- [Authentication](https://supabase.com/docs/guides/auth)

### Streamlit 공식 문서
- [Streamlit Docs](https://docs.streamlit.io)
- [Secrets Management](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Caching](https://docs.streamlit.io/library/advanced-features/caching)

### 관련 라이브러리
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Requests](https://requests.readthedocs.io/)

---

## ❓ FAQ

**Q: 데이터를 업데이트하려면?**
- A: Supabase 콘솔에서 직접 수정하면 5분 내에 대시보드에 반영됩니다 (캐시 때문)

**Q: 새로운 칼럼을 추가하려면?**
- A: 
  1. Supabase에서 칼럼 추가
  2. app.py의 column_mapping에 매핑 추가
  3. Streamlit 앱 재시작

**Q: 다른 테이블의 데이터도 표시하려면?**
- A:
  1. Supabase에서 테이블 생성
  2. app.py에서 새 함수 작성
  3. 필요한 부분에 추가

**Q: 보안 키는 왜 git에 커밋 안 함?**
- A: 민감한 정보 유출 방지. `.gitignore`로 제외하고 환경마다 다르게 관리

**Q: Streamlit Cloud 배포 후 데이터가 안 보이면?**
- A: 거의 항상 Secrets 미설정 문제. "Manage app" → "Secrets"에서 확인

---

## 📞 지원

문제 발생 시:
1. 📖 이 가이드의 "트러블슈팅" 섹션 확인
2. 🔍 Streamlit Cloud 로그 확인 ("View logs")
3. 🌐 Supabase 콘솔에서 데이터 확인
4. 💬 [Streamlit Community](https://discuss.streamlit.io/)

---

**마지막 업데이트:** 2026-06-04  
**작성자:** Claude Haiku 4.5
