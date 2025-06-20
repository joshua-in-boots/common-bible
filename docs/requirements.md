# 공동번역성서 프로젝트 요구사항

## 📌 개요

공동번역성서 개정판 원본 텍스트를 기반으로 각 장을 HTML 형식으로 변환한다. 본문 내 각 절에는 고유한 `id`를 부여하여, 본문 검색 시 해당 절로 바로 이동할 수 있도록 한다. (예: `<span id="창세-1-3">...</span>`)ML 형식으로 변환하고, 워드프레스를 통해 접근성 친화적으로 자동 게시하는 것을 목표로 한다. 또한, 시각 장애인을 위한 접근성을 고려하여 절 번호는 스크린리더에 표시되지 않도록 한다.

## 📂 입력 파일 구조

- 파일명: `common-bible-kr.txt`
- 전체 성경 본문이 포함되어 있음.
- 한 장의 본문은 다음 규칙에 따라 구분됨:

| 요소      | 설명                                                                |
| --------- | ------------------------------------------------------------------- |
| 장 시작   | `"창세 1:1"`, `"2마카 2:1"` 등의 형태로 시작 (숫자 앞머리는 선택적) |
| 절 번호   | 각 줄은 절 번호로 시작함 (예: `3 ¶ 하느님께서...`)                  |
| 단락 구분 | `¶` 기호가 단락(paragraph)의 시작을 표시함                          |
| 장 종료   | 각 장의 마지막에는 **두 줄의 빈 줄**이 있음                         |

## 📑 단락 구분 규칙

- `¶` 기호는 새 단락의 시작을 의미하므로 새 단락으로 구분한다.
- `¶` 기호가 없는 절은 이전 절과 같은 단락으로 간주한다.
- `¶` 기호 앞에 절 번호(verse-number)가 있는 경우, 절 번호는 단락 안에 포함되어야 한다.
- `¶` 기호가 단독으로 쓰이는 경우, `¶` 기호 전과 `¶` 기호 후는 모두 동일한 절이지만 단락을 나눠야 한다. `창세-1-4a`, `창세-1-4b` 등으로 분리하여 검색과 링크를 지원한다.

## 🧱 출력 HTML 구조

각 장은 하나의 HTML 파일 또는 워드프레스 포스트로 변환되며, 다음과 같은 시맨틱 구조를 가짐:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>창세기 1장</title>
  <link rel="stylesheet" href="verse-style.css">
</head>
<body>
  <!-- 절 검색 UI -->
  <div class="search-container">
    <input type="text" id="verse-search" placeholder="절 ID 입력 (예: 창세-1-3)">
    <button id="verse-search-btn">이동</button>
  </div>

  <article id="창세-1">
    <h1>창세기 1장</h1>

    <p>
      <span id="창세-1-1"><span aria-hidden="true" class="verse-number">1</span> <span class="paragraph-marker" aria-hidden="true">¶</span> 한처음에 하느님께서 하늘과 땅을 지어내셨다.</span>
      <span id="창세-1-2"><span aria-hidden="true" class="verse-number">2</span> 땅은 아직 모양을 갖추지 않고 아무것도 생기지 않았는데, 어둠이 깊은 물 위에...</span>
    </p>

    <p>
      <span id="창세-1-3"><span aria-hidden="true" class="verse-number">3</span> <span class="paragraph-marker" aria-hidden="true">¶</span> 하느님께서 "빛이 생겨라!" 하시자 빛이 생겨났다.</span>
      <span id="창세-1-4"><span aria-hidden="true" class="verse-number">4</span> 그 빛이 하느님 보시기에 좋았다. 하느님께서는 빛과 어둠을 나누시고...</span>
    </p>
  </article>

  <script src="verse-navigator.js"></script>
</body>
</html>
```

### ✅ 접근성 고려

| 방법                 | 목적                                                        | 적용 방식                                                                                                                |
| -------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `aria-hidden="true"` | 절 번호, `¶` 기호를 시각적으로 표시하되 스크린리더에선 숨김 | `<span aria-hidden="true" class="verse-number">1</span>`<br>`<span aria-hidden="true" class="paragraph-marker">¶</span>` |
| `id` 앵커            | 각 절에 직접 링크 가능                                      | `<span id="창세-1-3">...</span>`                                                                                         |

## ♿️ 시각 장애인을 위한 접근성 요구사항

- 스크린리더는 본문을 읽을 때 절 번호(예: "1", "2" 등)와 `¶` 기호를 읽지 않도록 한다. 이를 위해 절 번호에 `aria-hidden="true"` 속성을 사용하거나, 시각적으로만 표시하고 스크린리더에는 숨긴다.
- 본문 내 각 절에는 고유한 `id`를 부여하여, 본문 검색 시 해당 절로 바로 이동할 수 있도록 한다. (예: `<p id="창세-1-3">`)

## ⚙️ 자동화 구성 요소

### 1. 파서/변환기 (Python 스크립트)
- 입력 파일을 파싱하여 장/절 단위로 분할
- HTML 변환 템플릿에 맞춰 출력 파일 생성

### 2. HTML/CSS 스타일
- `verse-number` 등 스타일 정의
- WordPress 테마에 적용 가능

### 3. 게시 자동화
- 워드프레스 REST API를 사용한 자동 게시
  - `POST /wp-json/wp/v2/posts`
  - 제목, slug, 카테고리, 태그, 콘텐츠(body) 전달
  - **게시 상태**: `status: 'private'`로 설정하여 비공개 상태로 게시
  - 추후 일괄 공개: `status: 'publish'`로 업데이트하여 한꺼번에 공개 가능
- 대안: WP CLI 이용 (`wp post create --post_status=draft`)

## 🛠 워드프레스 설정 필요사항

| 항목          | 설명                                                                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| REST API 인증 | JWT Auth 플러그인, Application Password 등 사용                                                                                                         |
| 사용자 권한   | `editor` 또는 `administrator` 권한 필요                                                                                                                 |
| CSS 정의      | `Customizer`나 테마의 `style.css`에 접근성 관련 CSS 추가                                                                                                |
| 포스트 구성   | 각 장마다 별도의 포스트로 생성, 카테고리/태그 지정 가능<br>**초기 상태**: 비공개(`private`)로 생성<br>**일괄 공개**: 준비 완료 후 `publish` 상태로 변경 |

## 🔒 보안 요구사항

### API 보안
- **인증 토큰 관리**: Application Password 또는 JWT 토큰을 환경변수나 보안 설정 파일에 저장
- **HTTPS 통신**: 모든 REST API 호출은 HTTPS를 통해서만 수행
- **토큰 만료 관리**: JWT 토큰의 만료 시간 설정 및 자동 갱신 로직 구현
- **API 레이트 리미팅**: 과도한 요청 방지를 위한 요청 제한 설정

### 워드프레스 보안
- **사용자 권한 최소화**: 게시 전용 계정 생성 (`editor` 권한만 부여)
- **IP 제한**: 가능한 경우 특정 IP에서만 API 접근 허용
- **플러그인 보안**: 사용하는 인증 플러그인의 최신 버전 유지
- **백업**: 게시 전 데이터베이스 백업 수행

### 데이터 보안
- **입력 검증**: 성경 텍스트 파싱 시 악성 코드 삽입 방지
- **HTML 새니타이징**: 사용자 입력이 포함된 경우 XSS 방지 처리
- **로그 관리**: API 호출 및 오류 로그를 안전한 위치에 저장
- **민감 정보 제거**: 로그에 인증 토큰이나 비밀번호 기록 방지

## ✅ 요약 체크리스트

- [ ] 성경 장별 파싱 로직 구현
- [ ] 절 번호 + 본문을 HTML로 출력하는 템플릿 정의
- [ ] 접근성을 고려한 마크업 구성 (`aria-hidden`, `id` 앵커 등)
- [ ] 장별 HTML 파일 저장 또는 워드프레스 포스트로 업로드
- [ ] 워드프레스 REST API 인증 방식 준비
- [ ] 사용자 정의 스타일(CSS) 반영
- [ ] 보안 설정 구성 (HTTPS, 토큰 관리, 사용자 권한 등)
- [ ] 데이터 백업 및 로그 관리 체계 구축

