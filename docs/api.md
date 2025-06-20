# 공동번역성서 프로젝트 API 문서

## 📖 개요

이 문서는 공동번역성서 프로젝트의 주요 클래스와 함수들의 API를 설명합니다.

---

## 🔧 BibleParser 클래스

### 초기화

```python
parser = BibleParser(file_path: str)
```

**매개변수:**
- `file_path`: 공동번역성서 텍스트 파일 경로

### 메서드

#### `load_book_mappings() -> None`
성경 책 이름 매핑 데이터를 `data/bible_book_mappings.json`에서 로드합니다.

#### `identify_book(text: str) -> Optional[str]`
텍스트에서 성경 책 이름을 식별하여 전체 이름을 반환합니다.

**매개변수:**
- `text`: 분석할 텍스트 (예: "창세 1:1")

**반환값:**
- 성공 시: 전체 책 이름 (예: "창세기")
- 실패 시: `None`

#### `parse_file() -> List[Chapter]`
전체 파일을 파싱하여 장 단위로 분할합니다.

**반환값:**
- `List[Chapter]`: 파싱된 장들의 목록

#### `parse_chapter(chapter_text: str) -> Chapter`
개별 장을 파싱하여 절 단위로 분할합니다.

**매개변수:**
- `chapter_text`: 장 텍스트

**반환값:**
- `Chapter`: 파싱된 장 객체

#### `parse_verse(verse_text: str) -> Verse`
절 텍스트를 파싱하여 단락 구분을 처리합니다.

**매개변수:**
- `verse_text`: 절 텍스트

**반환값:**
- `Verse`: 파싱된 절 객체

---

## 🎨 HTMLGenerator 클래스

### 초기화

```python
generator = HTMLGenerator(template_path: str)
```

**매개변수:**
- `template_path`: HTML 템플릿 파일 경로

### 메서드

#### `generate_chapter_html(chapter: Chapter) -> str`
장 단위 HTML을 생성합니다.

**매개변수:**
- `chapter`: 장 객체

**반환값:**
- `str`: 생성된 HTML 문자열

#### `generate_verse_span(verse: Verse) -> str`
절 HTML 요소를 생성합니다.

**매개변수:**
- `verse`: 절 객체

**반환값:**
- `str`: 절 HTML 문자열

#### `apply_accessibility_attributes(element: str) -> str`
접근성 속성을 적용합니다.

**매개변수:**
- `element`: HTML 요소 문자열

**반환값:**
- `str`: 접근성 속성이 적용된 HTML

---

## 🚀 WordPressPublisher 클래스

### 초기화

```python
publisher = WordPressPublisher(wp_url: str, auth_token: str)
```

**매개변수:**
- `wp_url`: 워드프레스 사이트 URL
- `auth_token`: 인증 토큰

### 메서드

#### `validate_auth() -> bool`
인증 상태를 확인합니다.

**반환값:**
- `bool`: 인증 성공 여부

#### `publish_chapter(chapter: Chapter, html_content: str) -> bool`
개별 장을 워드프레스에 게시합니다.

**매개변수:**
- `chapter`: 장 객체
- `html_content`: HTML 콘텐츠

**반환값:**
- `bool`: 게시 성공 여부

#### `batch_publish_all(chapters: List[Chapter]) -> List[str]`
모든 장을 일괄 공개합니다.

**매개변수:**
- `chapters`: 장 객체들의 목록

**반환값:**
- `List[str]`: 게시된 포스트 ID 목록

---

## 📊 데이터 모델

### Chapter 클래스

```python
@dataclass
class Chapter:
    book_name: str          # 책 이름 (예: "창세기")
    chapter_number: int     # 장 번호 (예: 1)
    verses: List[Verse]     # 절 목록
    id: str                # 장 ID (예: "창세-1")
```

### Verse 클래스

```python
@dataclass
class Verse:
    number: int             # 절 번호 (예: 1)
    text: str              # 절 텍스트
    has_paragraph: bool    # ¶ 기호 유무
    sub_parts: List[str]   # 단독 ¶로 분할된 경우
    id: str               # 절 ID (예: "창세-1-1")
```

---

## 🌐 JavaScript API (verse-navigator.js)

### 함수

#### `parseSearchInput(input: string) -> string[]`
검색 입력을 절 ID 배열로 변환합니다.

**매개변수:**
- `input`: 검색 입력 (예: "창세 1:1-3")

**반환값:**
- `string[]`: 절 ID 배열 (예: ["창세-1-1", "창세-1-2", "창세-1-3"])

#### `goToVerse(searchInput: string) -> void`
검색된 절로 이동하고 하이라이트합니다.

**매개변수:**
- `searchInput`: 검색 입력

#### 지원하는 검색 형식
- `"창세-1-3"`: 직접 ID 형식
- `"창세기 1:3"`: 전체 책 이름 + 장:절
- `"창세 1:3"`: 약칭 + 장:절
- `"창세 1:1-5"`: 범위 검색

---

## 🔒 SecurityManager 클래스

### 메서드

#### `load_credentials() -> None`
환경변수에서 인증 정보를 로드합니다.

#### `validate_https(url: str) -> bool`
HTTPS 연결을 검증합니다.

**매개변수:**
- `url`: 검증할 URL

**반환값:**
- `bool`: HTTPS 여부

#### `sanitize_input(text: str) -> str`
입력 데이터를 새니타이징합니다.

**매개변수:**
- `text`: 새니타이징할 텍스트

**반환값:**
- `str`: 새니타이징된 텍스트

---

## ⚠️ 예외 처리

### ParseError
텍스트 파싱 중 발생하는 오류

### AuthenticationError
워드프레스 인증 실패 시 발생

### PublishError
게시 중 발생하는 오류

---

## 📋 사용 예시

### 기본 파이프라인

```python
# 1. 파싱
parser = BibleParser('data/common-bible-kr.txt')
chapters = parser.parse_file()

# 2. HTML 생성
generator = HTMLGenerator('templates/chapter_template.html')
html_content = generator.generate_chapter_html(chapters[0])

# 3. 워드프레스 게시
publisher = WordPressPublisher(
    wp_url=os.getenv('WP_BASE_URL'),
    auth_token=os.getenv('WP_AUTH_TOKEN')
)

if publisher.validate_auth():
    success = publisher.publish_chapter(chapters[0], html_content)
    print(f"게시 결과: {success}")
```

### 책 이름 식별

```python
parser = BibleParser('data/common-bible-kr.txt')
book_name = parser.identify_book("창세 1:1")  # "창세기"
book_name = parser.identify_book("마태 5:3")  # "마태오의 복음서"
```

### JavaScript 검색

```javascript
// 다양한 검색 방식
goToVerse("창세-1-3");              // 직접 ID
goToVerse("창세기 1:3");            // 전체 이름
goToVerse("창세 1:1-5");            // 범위 검색
```
