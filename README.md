# 공동번역성서 프로젝트

대한성공회 서울교구 홈페이지에 공동번역성서를 게시하는 작업을 위한 프로젝트입니다. 공동번역성서 개정판 원본 텍스트를 HTML로 변환하고, 워드프레스를 통해 접근성 친화적으로 자동 게시하고자 합니다.

이 프로젝트는 바이브코딩으로 얼마나 코딩이 가능한지 검증하는 사심 가득한 프로젝트로, 모든 문서와 코드는 바이브코딩으로 생성했습니다. 실제 공동번역성서 개정판의 저작권은 대한성서공회에 있으며, 이 프로젝트는 비상업적 용도로만 사용됩니다. 공동번역성서 개정판 텍스트를 요구하지 말아주세요.

## 🎯 프로젝트 목표

- 성경 텍스트를 장/절 단위로 파싱하여 구조화된 HTML로 변환
- 시각 장애인을 위한 웹 접근성 준수 (WCAG 2.1 AA)
- 워드프레스 REST API를 통한 자동 게시
- 절 번호 기반 검색 및 직접 링크 기능

## 📋 주요 기능

### ✨ 텍스트 처리
- 공동번역성서 텍스트 파일 자동 파싱
- 성경 책 이름 매핑 데이터 활용 (약칭 → 전체 이름)
- 장/절 단위 구조 분석
- `¶` 기호 기반 단락 구분 처리
- 절 세분화 지원 (`창세-1-4a`, `창세-1-4b`)

### ♿️ 웹 접근성
- 스크린리더가 본문을 읽을 때에는 절 번호를 읽지 않도록 처리 (`aria-hidden="true"`)
- 절 번호를 검색할 때에는 접근 가능하도록 처리
- 각 절별 고유 ID를 통한 직접 링크
- 시맨틱 HTML 구조 (`<article>`, `<section>`)
- 키보드 네비게이션 지원

### 🔍 검색 기능
- 절 ID 기반 빠른 이동 (`창세-1-3`)
- URL 해시를 통한 직접 접근 (`#창세-1-3`)
- 하이라이트 효과로 시각적 피드백

### 🚀 자동 게시
- 워드프레스 REST API 연동
- 비공개 상태 초기 업로드
- 준비 완료 후 일괄 공개
- 오류 처리 및 재시도 로직

## 🏗️ 프로젝트 구조

```
common-bible/
├── docs/                   # 문서
│   ├── requirements.md     # 요구사항 명세
│   ├── design-specification.md # 설계서
│   ├── verse-style.css     # 스타일시트
│   └── verse-navigator.js  # 검색/네비게이션 스크립트
├── src/                    # 소스코드
│   ├── parser.py          # 텍스트 파싱 엔진
│   ├── html_generator.py  # HTML 생성기
│   ├── wp_publisher.py    # 워드프레스 게시 클래스
│   └── config.py          # 설정 관리
├── templates/             # HTML 템플릿
├── data/                  # 데이터 파일
│   ├── common-bible-kr.txt # 원본 텍스트
│   ├── bible_book_mappings.json # 성경 책 이름 매핑
│   └── output/            # 생성된 HTML
├── config/               # 설정 파일
├── logs/                 # 로그 파일
└── tests/                # 테스트
```

## 📊 데이터 구조

### 성경 책 이름 매핑
프로젝트는 `data/bible_book_mappings.json`을 사용하여 성경 책의 약칭을 전체 이름으로 변환합니다:

```json
{
  "약칭": "창세",
  "전체 이름": "창세기", 
  "영문 이름": "Genesis"
}
```

이를 통해 다음과 같은 변환이 가능합니다:
- `"창세 1:1"` → `"창세기 1장"`
- `"2마카 2:1"` → `"마카베오하 2장"`

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone git@github.com:joshua-in-boots/common-bible.git
cd common-bible

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
# 환경변수 파일 생성
cp config/.env.example config/.env

# .env 파일 편집
nano config/.env
```

필수 환경변수:
```env
WP_BASE_URL=https://your-wordpress-site.com
WP_AUTH_TOKEN=your_application_password
WP_API_RATE_LIMIT=60
LOG_LEVEL=INFO
```

### 3. 실행

```bash
# 텍스트 파싱
python src/parser.py --input data/common-bible-kr.txt

# HTML 생성
python src/html_generator.py --chapters data/output/chapters.json

# 워드프레스 게시 (테스트)
python src/wp_publisher.py --test-auth

# 실제 게시 (비공개)
python src/wp_publisher.py --upload-all --status=private
```

## 📖 사용법

### 기본 파싱 및 변환

```python
from src.parser import BibleParser
from src.html_generator import HTMLGenerator

# 파싱 (성경 책 이름 매핑 자동 로드)
parser = BibleParser('data/common-bible-kr.txt')
chapters = parser.parse_file()

# 책 이름 식별 예시
book_name = parser.identify_book("창세 1:1")  # "창세기" 반환

# HTML 생성
generator = HTMLGenerator('templates/chapter_template.html')
html_content = generator.generate_chapter_html(chapters[0])
```

### 워드프레스 게시

```python
from src.wp_publisher import WordPressPublisher

# 게시자 초기화
publisher = WordPressPublisher(
    wp_url=os.getenv('WP_BASE_URL'),
    auth_token=os.getenv('WP_AUTH_TOKEN')
)

# 개별 장 게시
success = publisher.publish_chapter(chapter, html_content)

# 일괄 공개
published_ids = publisher.batch_publish_all(chapters)
```

## 🧪 테스트

```bash
# 전체 테스트 실행
python -m pytest tests/

# 특정 모듈 테스트
python -m pytest tests/test_parser.py -v

# 커버리지 포함 테스트
python -m pytest --cov=src tests/
```

## 📝 HTML 출력 예시

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>창세기 1장</title>
  <link rel="stylesheet" href="verse-style.css">
</head>
<body>
  <article id="창세-1">
    <h1>창세기 1장</h1>
    
    <p>
      <span id="창세-1-1">
        <span aria-hidden="true" class="verse-number">1</span>
        <span aria-hidden="true" class="paragraph-marker">¶</span>
        한처음에 하느님께서 하늘과 땅을 지어내셨다.
      </span>
    </p>
    
    <p>
      <span id="창세-1-2">
        <span aria-hidden="true" class="verse-number">2</span>
        땅은 아직 모양을 갖추지 않고...
      </span>
    </p>
  </article>
  
  <script src="verse-navigator.js"></script>
</body>
</html>
```

## 🔒 보안 고려사항

- 모든 인증 정보는 환경변수로 관리
- HTTPS 통신만 허용
- 입력 데이터 새니타이징
- API 레이트 리미팅

## 📚 문서

- [요구사항 명세서](docs/requirements.md)
- [상세 설계서](docs/design-specification.md)

## 🤝 기여하기

1. 이슈 등록 또는 기능 제안
2. Fork 및 브랜치 생성
3. 코드 작성 및 테스트
4. Pull Request 제출

### 개발 가이드라인

- PEP 8 코딩 스타일 준수
- 모든 기능에 대한 단위 테스트 작성
- 접근성 가이드라인 (WCAG 2.1 AA) 준수
- 보안 모범 사례 적용

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE) 하에 배포됩니다.

## 🙏 감사의 말

- 공동번역성서 개정판을 제공해주신 모든 분들께 감사드립니다.
- 웹 접근성 개선에 기여하는 모든 개발자들께 감사드립니다.

---

## 📞 문의

프로젝트 관련 문의사항이나 버그 리포트는 [이슈 페이지](../../issues)를 이용해 주세요.
