# 공동번역성서 프로젝트 설계서

## 📋 개요

본 설계서는 공동번역성서 텍스트 파일을 파싱하여 HTML로 변환하고, 워드프레스를 통해 접근성 친화적으로 게시하는 시스템의 상세 설계를 다룹니다.

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input File    │ -> │   Parser/        │ -> │   WordPress     │
│ common-bible-   │    │   Converter      │    │   Publishing    │
│   kr.txt        │    │   (Python)       │    │   (REST API)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              v
                       ┌──────────────────┐
                       │   HTML Output    │
                       │   + CSS/JS       │
                       └──────────────────┘
```

---

## 📂 프로젝트 구조

```
common-bible/
├── src/
│   ├── __init__.py         # 패키지 초기화
│   ├── parser.py           # 텍스트 파싱 엔진
│   ├── models.py           # 데이터 모델 클래스
│   ├── html_generator.py   # HTML 생성기
│   ├── wp_publisher.py     # 워드프레스 게시 클래스
│   ├── config.py           # 설정 관리
│   ├── security.py         # 보안 관리
│   ├── logger.py           # 로깅 시스템
│   ├── cli.py              # 명령줄 인터페이스
│   └── main.py             # 메인 실행 모듈
├── templates/
│   └── chapter_template.html
├── static/
│   ├── verse-style.css
│   └── verse-navigator.js
├── data/
│   ├── common-bible-kr.txt
│   ├── bible_book_mappings.json  # 성경 책 이름 매핑 데이터
│   └── output/             # 생성된 HTML 파일들
├── config/
│   └── .env.example        # 환경변수 예제 (보안)
├── logs/                   # 로그 저장 디렉터리
├── tests/
│   ├── test_parser.py
│   ├── test_html_generator.py
│   ├── test_wp_publisher.py
│   └── test_integration.py
├── docs/
│   ├── requirements.md     # 요구사항 문서
│   ├── design-specification.md  # 설계 문서
│   ├── api.md              # API 문서
│   └── deployment.md       # 배포 가이드
├── CHANGELOG.md            # 변경사항 기록
├── CONTRIBUTING.md         # 기여 가이드
├── LICENSE                 # 라이선스
├── README.md               # 프로젝트 설명
└── requirements.txt        # 의존성 패키지 목록
```

---

## 🔧 핵심 컴포넌트 설계

### 1. 텍스트 파서 (parser.py)

```python
class BibleParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.chapters = []
        self.load_book_mappings()
    
    def load_book_mappings(self) -> None:
        """성경 책 이름 매핑 데이터 로드"""
        with open('data/bible_book_mappings.json', 'r', encoding='utf-8') as f:
            self.book_mappings = json.load(f)
    
    def identify_book(self, text: str) -> Optional[str]:
        """텍스트에서 성경 책 이름 식별"""
        for book in self.book_mappings:
            if text.startswith(book['약칭']):
                return book['전체 이름']
        return None
    
    def parse_file(self) -> List[Chapter]:
        """전체 파일을 파싱하여 장 단위로 분할"""
        pass
    
    def parse_chapter(self, chapter_text: str) -> Chapter:
        """개별 장을 파싱하여 절 단위로 분할"""
        pass
    
    def parse_verse(self, verse_text: str) -> Verse:
        """절 텍스트를 파싱하여 단락 구분 처리"""
        pass
```

**주요 기능:**
- 성경 책 이름 매핑 데이터 로드 (`bible_book_mappings.json`)
- 장 시작 패턴 인식 (`"창세 1:1"`, `"2마카 2:1"` 등)
- 약칭에서 전체 이름으로 변환 (`"창세"` → `"창세기"`)
- 절 번호 추출 및 본문 분리
- `¶` 기호 기반 단락 구분 처리
- 단독 `¶` 기호 시 절 세분화 (`창세-1-4a`, `창세-1-4b`)

### 2. HTML 생성기 (html_generator.py)

```python
class HTMLGenerator:
    def __init__(self, template_path: str):
        self.template_path = template_path
    
    def generate_chapter_html(self, chapter: Chapter) -> str:
        """장 단위 HTML 생성"""
        pass
    
    def generate_verse_span(self, verse: Verse) -> str:
        """절 HTML 요소 생성 (접근성 고려)"""
        pass
    
    def apply_accessibility_attributes(self, element: str) -> str:
        """접근성 속성 적용"""
        pass
```

**주요 기능:**
- 시맨틱 HTML 구조 생성 (`<article>`, `<h1>`, `<p>`, `<span>`)
- 절 번호에 `aria-hidden="true"` 적용
- 고유한 ID 생성 (`창세-1-3`, `창세-1-4a` 등)
- CSS/JS 파일 링크 포함

### 3. 워드프레스 게시자 (wp_publisher.py)

```python
class WordPressPublisher:
    def __init__(self, wp_url: str, auth_token: str):
        self.wp_url = wp_url
        self.auth_token = auth_token
        self.session = requests.Session()
    
    def publish_chapter(self, chapter: Chapter, html_content: str) -> bool:
        """개별 장을 워드프레스에 게시"""
        pass
    
    def batch_publish_all(self, chapters: List[Chapter]) -> List[str]:
        """모든 장을 일괄 공개"""
        pass
    
    def validate_auth(self) -> bool:
        """인증 상태 확인"""
        pass
```

**주요 기능:**
- REST API를 통한 포스트 생성 (`POST /wp-json/wp/v2/posts`)
- 초기 `private` 상태로 게시
- 일괄 `publish` 상태 변경
- 오류 처리 및 재시도 로직

---

## 📊 데이터 파일 구조

### 성경 책 이름 매핑 (bible_book_mappings.json)
```json
[
  {
    "약칭": "창세",
    "전체 이름": "창세기",
    "영문 이름": "Genesis"
  },
  {
    "약칭": "출애",
    "전체 이름": "출애굽기",
    "영문 이름": "Exodus"
  }
  // ... 총 66권의 성경 책 매핑
]
```

**용도:**
- 텍스트 파싱 시 책 이름 식별
- 약칭을 전체 이름으로 변환
- 다국어 지원을 위한 영문 이름 제공

---

## 📊 데이터 모델

### Bible 클래스
```python
@dataclass
class Bible:
    title: str              # "공동번역성서"
    books: List[Book]        # 책 객체 리스트
    language: str = "ko"     # 언어
```

### Book 클래스
```python
@dataclass
class Book:
    name: str               # "창세기"
    abbr: str               # "창세"
    chapters: List[Chapter]  # 장 객체 리스트
    eng_name: str = ""       # "Genesis"
    id: str = ""            # "창세"
```

### Chapter 클래스
```python
@dataclass
class Chapter:
    book_name: str          # "창세기"
    chapter_number: int     # 1
    verses: List[Verse]      # 절 객체 리스트
    id: str = ""            # "창세-1"
    book_abbr: str = ""     # "창세"
```

### Verse 클래스
```python
@dataclass
class Verse:
    number: int             # 1
    text: str               # "한처음에 하느님께서..."
    has_paragraph: bool = False  # ¶ 기호 유무
    sub_parts: List[str] = field(default_factory=list)  # 단독 ¶로 분할된 경우
    id: str = ""            # "창세-1-1" or "창세-1-4a"
```

---

## 🔒 보안 설계

### 보안 관리자 (security.py)
```python
class SecurityManager:
    def __init__(self):
        """보안 관리자 초기화"""
        self.wp_token = None
        self.wp_url = None
        self.load_credentials()
    
    def load_credentials(self) -> None:
        """환경변수에서 인증 정보 로드"""
        self.wp_token = os.getenv('WP_AUTH_TOKEN')
        self.wp_url = os.getenv('WP_BASE_URL')
    
    def validate_https(self, url: str) -> bool:
        """HTTPS 연결 검증"""
        if not url:
            return False
        parsed = urlparse(url)
        return parsed.scheme == 'https'
    
    def sanitize_input(self, text: str) -> str:
        """입력 텍스트 새니타이징"""
        if not text:
            return ""
        return html.escape(text)
    
    def sanitize_html_content(self, content: str) -> str:
        """HTML 콘텐츠 새니타이징 (XSS 방지)"""
        if not content:
            return ""
        # 스크립트 태그 및 위험 요소 제거
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        return content
    
    def generate_signature(self, data: str, key: Optional[str] = None) -> str:
        """HMAC 서명 생성"""
        if key is None:
            key = self.wp_token or 'default-key'
        h = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
        return base64.b64encode(h.digest()).decode('utf-8')
```

### 환경변수 (.env.example)
```
# WordPress API 설정
WP_BASE_URL=https://your-wordpress-site.com
WP_AUTH_TOKEN=your_application_password
WP_API_RATE_LIMIT=60

# 로깅 설정
LOG_LEVEL=INFO
LOG_TO_CONSOLE=true
LOG_COLOR=true

# 보안 설정
VERIFY_SSL=true
```

---

## 🎨 프론트엔드 설계

### CSS 구조 (verse-style.css)
```css
/* 기본 레이아웃 */
.search-container { /* 검색 UI 스타일 */ }
article { /* 장 컨테이너 */ }
article h1 { /* 장 제목 */ }
article p { /* 절 컨테이너 */ }

/* 접근성 요소 */
.verse-number { color: #888; /* 절 번호 */ }
.paragraph-marker { color: #888; /* 단락 표시 */ }
[aria-hidden="true"] { /* 스크린리더 숨김 */ }

/* 반응형 디자인 */
@media (max-width: 768px) { /* 모바일 최적화 */ }
```

### JavaScript 기능 (verse-navigator.js)
```javascript
class VerseNavigator {
    constructor() {
        this.initializeEventListeners();
        this.handleUrlHash();
    }
    
    goToVerse(verseId) {
        // 절 이동 및 하이라이트
    }
    
    initializeEventListeners() {
        // 검색 박스 이벤트 바인딩
    }
    
    handleUrlHash() {
        // URL 해시 기반 자동 이동
    }
}
```

---

## 🚀 배포 및 실행 흐름

### 1. 개발 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp config/.env.example config/.env
# .env 파일 편집

# 테스트 실행
python -m pytest tests/
```

### 2. CLI 도구 사용 (cli.py)
```bash
# 시스템 정보 확인
python -m src.cli info

# 텍스트 파싱
python -m src.cli parse --input data/common-bible-kr.txt --split

# HTML 생성
python -m src.cli generate --input data/output/chapters

# 워드프레스 인증 테스트
python -m src.cli publish --test

# 워드프레스에 비공개로 게시
python -m src.cli publish --status private

# 일괄 공개로 상태 변경
python -m src.cli update-status --status publish

# 전체 파이프라인 실행
python -m src.cli pipeline --status private
```

### 3. 메인 모듈 사용 (main.py)
```bash
# 전체 파이프라인 실행
python -m src.main --full-pipeline

# 텍스트 파싱만 실행
python -m src.main --parse --input data/common-bible-kr.txt --split-chapters

# HTML 생성만 실행
python -m src.main --generate-html --json-input data/output/chapters

# 워드프레스 게시만 실행
python -m src.main --publish --status private

# 인증 테스트만 실행
python -m src.main --test-auth
```

---

## 📈 성능 및 확장성

### 처리 성능
- **목표**: 66권 1,189장 처리 시간 < 10분
- **병렬 처리**: 장별 HTML 생성 멀티스레딩
- **메모리 관리**: 대용량 파일 스트리밍 파싱

### 확장성 고려사항
- **다국어 지원**: 언어별 설정 파일 분리
- **템플릿 시스템**: 다양한 HTML 템플릿 지원
- **플러그인 아키텍처**: 추가 변환기 모듈 지원

---

## 🧪 테스트 전략

### 단위 테스트
- 파서 기능별 테스트 (장/절/단락 분리)
- HTML 생성 결과 검증
- 접근성 속성 정확성 확인

### 통합 테스트
- 전체 파이프라인 테스트
- 워드프레스 API 연동 테스트
- 실제 데이터를 이용한 E2E 테스트

### 성능 테스트
- 대용량 파일 처리 성능
- 메모리 사용량 모니터링
- API 호출 지연시간 측정

---

## 📝 운영 가이드

### 로깅 시스템 (logger.py)
```python
class Logger:
    """로거 클래스"""
    
    _instance = None  # 싱글톤 인스턴스
    
    def __init__(self):
        """로거 초기화"""
        if self._initialized:
            return
        
        self._initialized = True
        self.loggers = {}  # 이름별 로거 캐시
    
    def setup(self, log_level: str = 'INFO',
              log_file: Optional[str] = None,
              log_to_console: bool = True,
              use_color: bool = True) -> None:
        """로깅 시스템 설정"""
        # 로그 레벨 설정
        log_level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        level = log_level_map.get(log_level.upper(), logging.INFO)
        
        # 로그 디렉토리 및 파일 설정
        if log_file is None:
            timestamp = time.strftime('%Y%m%d')
            log_file = f'logs/bible_converter_{timestamp}.log'
        
        # 파일 핸들러 (RotatingFileHandler 사용)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        
        # 콘솔 핸들러 (컬러 지원)
        if log_to_console and use_color:
            color_formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                }
            )
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(color_formatter)
```

### 백업 및 복구
- 변환 전 원본 파일 백업
- 워드프레스 데이터베이스 백업
- 생성된 HTML 파일 버전 관리

### 오류 처리
- API 호출 실패 시 재시도 로직
- 파싱 오류 시 수동 확인 대상 로깅
- 부분 실패 시 중단점에서 재시작 가능

---

## ✅ 구현 마일스톤

### Phase 1: 기본 설계 및 모델 구현 (완료)
- [x] 프로젝트 구조 설계
- [x] 데이터 모델 구현 (모델, 설정, 로깅)
- [x] 성경 책 매핑 데이터 정의

### Phase 2: 기본 파싱 및 변환 (현재 진행 중)
- [x] 텍스트 파서 구현
- [x] HTML 생성기 구현
- [x] 단위 테스트 작성
- [ ] 성능 최적화 (대용량 파일 처리)

### Phase 3: 워드프레스 연동 (예정)
- [x] REST API 클라이언트 기본 구현
- [x] 인증 및 보안 설정
- [ ] 게시물 메타데이터 관리
- [ ] 통합 테스트 강화

### Phase 4: UI/UX 및 접근성 (예정)
- [x] 기본 CSS/JavaScript 구현
- [ ] 사용자 인터페이스 개선
- [ ] 접근성 테스트 및 개선
- [ ] 반응형 디자인 완료

### Phase 5: 배포 및 최적화 (예정)
- [ ] 전체 시스템 성능 최적화
- [x] CLI 도구 완성
- [x] 문서화 완료
- [ ] 프로덕션 배포

이 설계서를 기반으로 단계별 구현을 진행하시면 됩니다. 추가로 상세히 다뤄야 할 부분이 있으면 말씀해 주세요.
