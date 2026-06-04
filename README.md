# 홈앤쇼핑 일일 매출 현황 대시보드

실시간 주문 데이터 분석 및 시각화 Streamlit 대시보드

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR_STREAMLIT_CLOUD_URL)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/github-tqqq3xm--droid/test-blue?logo=github)](https://github.com/tqqq3xm-droid/test)

---

## 🎯 개요

홈앤쇼핑의 일일 매출 현황을 한눈에 파악할 수 있는 대시보드입니다.

**주요 기능:**
- 📊 **일별 매출 추이:** 시간 흐름에 따른 매출 변화
- 📈 **카테고리별 분석:** 상품 카테고리별 매출 비중
- 💰 **일일 비교:** 오늘 vs 어제 매출 비교
- 📉 **성장률 분석:** 어제 대비 증감률 즉시 확인

---

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/tqqq3xm-droid/test.git
cd test
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Secrets 설정

`.streamlit/secrets.toml` 파일 생성:

```toml
SUPABASE_URL = "https://grbbbrgrcplvfettmlyq.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
```

### 4. 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 📦 필요 요구사항

- Python 3.8 이상
- Supabase 프로젝트 (테이블 및 API 키)
- pip

**의존성 패키지:**
```
streamlit >= 1.0
pandas >= 1.3.0
plotly >= 5.0
```

자세한 내용은 [requirements.txt](requirements.txt) 참고

---

## 🔧 설정

### 환경 변수 (`.streamlit/secrets.toml`)

| 변수 | 설명 | 예시 |
|------|------|------|
| SUPABASE_URL | Supabase 프로젝트 URL | `https://xxxx.supabase.co` |
| SUPABASE_KEY | Supabase Anon API 키 | `eyJhbGc...` |

### Streamlit 설정

Streamlit Cloud에서:
1. "Manage app" → "Secrets"
2. TOML 형식으로 위 환경 변수 입력
3. "Save" 클릭

자세한 내용은 [SETUP_GUIDE.md](SETUP_GUIDE.md) 참고

---

## 📊 데이터베이스

### Supabase 테이블: `orders`

```
프로젝트 ID: grbbbrgrcplvfettmlyq
리전: ap-northeast-2 (서울)
```

**테이블 구조:**
- order_id (TEXT): 주문 ID
- order_date (DATE): 주문 날짜
- product (TEXT): 상품명
- category (TEXT): 카테고리
- team (TEXT): 팀
- media (TEXT): 판매 매체
- product_sales (INTEGER): 상품취급액
- ... 및 12개 추가 금액 관련 칼럼

자세한 내용: [SETUP_GUIDE.md#데이터베이스-구조](SETUP_GUIDE.md#데이터베이스-구조)

---

## 📈 주요 기능

### 1. 일별 매출 추이

시간 흐름에 따른 매출 변화를 선 그래프로 시각화

```
│ 매출
│     ●
│    ╱ ╲    ●
│   ╱   ╲  ╱ ╲
└──●─────●────────► 날짜
```

### 2. 카테고리별 매출 비중

원형 차트로 각 카테고리의 매출 비중 표시

```
         뷰티 30%
    ┌─────────┐
패션 │         │ 생활용품
20%  │ 대시보드│ 25%
     │         │
    └─────────┘
  전자 15%, 식품 10%
```

### 3. 오늘/어제 비교

```
┌─────────────────┬──────────────┬──────────────┐
│  오늘 매출      │ 어제 매출    │ 증감률       │
├─────────────────┼──────────────┼──────────────┤
│ ₩1,500,000      │ ₩1,200,000   │ +25.0%       │
└─────────────────┴──────────────┴──────────────┘
```

---

## 🌐 배포

### Streamlit Cloud 배포

```bash
# 1. GitHub에 코드 푸시
git push origin main

# 2. Streamlit Cloud에서 앱 배포
# https://share.streamlit.io → "New app" → GitHub 저장소 선택

# 3. Secrets 설정
# "Manage app" → "Secrets" → TOML 입력 → "Save"
```

**배포된 앱:** `https://your-app-name.streamlit.app`

자세한 내용: [SETUP_GUIDE.md#streamlit-cloud-배포](SETUP_GUIDE.md#streamlit-cloud-배포)

---

## 📁 프로젝트 구조

```
test/
├── app.py                      # Streamlit 메인 앱
├── requirements.txt            # Python 의존성
├── README.md                   # 이 파일
├── SETUP_GUIDE.md             # 상세 설정 가이드
├── 주문_데이터.csv             # 원본 데이터
├── .gitignore                 # Git 제외 설정
│
├── .streamlit/
│   └── secrets.toml           # Supabase 설정 (git 제외)
│
└── .git/                      # Git 저장소
```

---

## 💻 개발

### 로컬 개발 환경

```bash
# 저장소 클론
git clone https://github.com/tqqq3xm-droid/test.git
cd test

# 가상 환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
streamlit run app.py --logger.level=debug
```

### 코드 수정 시 주의사항

1. **Secrets 보안:** API 키를 git에 커밋하지 마세요
2. **캐시 설정:** `@st.cache_data(ttl=300)`으로 성능 최적화
3. **에러 처리:** Streamlit Cloud와 로컬 모두 지원하도록
4. **한글 지원:** UTF-8 인코딩 유지

### 새 기능 추가 예시

```python
# Supabase에서 새 테이블 데이터 로드
@st.cache_data(ttl=300)
def load_new_data():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    response = requests.get(
        f'{url}/rest/v1/new_table?select=*',
        headers=headers
    )
    return pd.DataFrame(response.json())

# 사용
df = load_new_data()
st.dataframe(df)
```

---

## 🔍 API 엔드포인트

### Supabase REST API

```
GET /rest/v1/orders
Authorization: Bearer YOUR_ANON_KEY
```

**응답 예:**

```json
[
  {
    "id": 1,
    "order_id": "ORD001",
    "order_date": "2026-06-01",
    "product": "시그니처 세트A",
    "category": "뷰티",
    "product_sales": 150000,
    ...
  }
]
```

자세한 내용: [SETUP_GUIDE.md#supabase-설정](SETUP_GUIDE.md#supabase-설정)

---

## 🐛 트러블슈팅

### "Invalid API key" 오류

```bash
# 1. secrets.toml 확인
cat .streamlit/secrets.toml

# 2. API 키 유효성 테스트
curl -H "apikey: YOUR_KEY" \
     "https://grbbbrgrcplvfettmlyq.supabase.co/rest/v1/orders"

# 3. Streamlit 재시작
streamlit run app.py
```

### 데이터가 없는 경우

1. ✅ Supabase 콘솔에서 orders 테이블 확인
2. ✅ 데이터 존재 여부 확인
3. ✅ API 엔드포인트 테스트

자세한 내용: [SETUP_GUIDE.md#트러블슈팅](SETUP_GUIDE.md#트러블슈팅)

---

## 📚 추가 자료

- **설정 가이드:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Supabase 문서:** https://supabase.com/docs
- **Streamlit 문서:** https://docs.streamlit.io
- **Plotly 문서:** https://plotly.com/python/

---

## 🤝 기여

이 프로젝트에 기여하고 싶으신가요?

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

---

## 📊 변경 이력

### v1.0.0 - 2026-06-04

**초기 릴리스**
- ✅ Streamlit 대시보드 구현
- ✅ Supabase 데이터베이스 연동
- ✅ 일별 매출 추이 차트
- ✅ 카테고리별 매출 분석
- ✅ 실시간 데이터 업데이트

**커밋:**
```
2ea9b02 - Connect Streamlit to Supabase with secrets.toml configuration
d3c1d3e - Improve Streamlit Cloud compatibility with better error handling
```

---

## 👨‍💻 개발자

- **작성자:** Claude Haiku 4.5
- **팀:** 홈앤쇼핑 데이터팀
- **마지막 업데이트:** 2026-06-04

---

## 📞 지원

문제나 질문이 있으신가요?

1. 📖 [SETUP_GUIDE.md](SETUP_GUIDE.md)의 FAQ 섹션 확인
2. 🐛 [Issues](https://github.com/tqqq3xm-droid/test/issues) 생성
3. 💬 [Discussions](https://github.com/tqqq3xm-droid/test/discussions) 시작

---

**Happy Analyzing! 📊**
