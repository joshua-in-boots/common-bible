# 기여 가이드

공동번역성서 프로젝트에 기여해 주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 방법을 안내합니다.

## 🎯 기여 방법

### 1. 이슈 리포팅
- 버그 발견 시 GitHub Issues에 상세한 내용 기록
- 기능 제안은 Feature Request 템플릿 사용
- 재현 가능한 예시와 함께 제출

### 2. 코드 기여
1. Repository Fork
2. Feature Branch 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. Branch에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

### 3. 문서 개선
- 오타 수정, 설명 개선, 예시 추가 등
- API 문서 업데이트
- 다국어 번역 지원

## 📝 코딩 스타일

### Python
- PEP 8 스타일 가이드 준수
- Black 포매터 사용: `black src/`
- Flake8 린터 통과: `flake8 src/`

### JavaScript
- ES6+ 문법 사용
- 2-space 들여쓰기
- 세미콜론 사용

### 커밋 메시지
```
type(scope): description

[optional body]

[optional footer]
```

**Type:**
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포매팅
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `chore`: 기타 작업

## 🧪 테스트

### 로컬 테스트
```bash
# 전체 테스트
python -m pytest tests/

# 커버리지 포함
python -m pytest --cov=src tests/

# 특정 모듈
python -m pytest tests/test_parser.py -v
```

### 코드 품질 검사
```bash
# 포매팅
black src/ tests/

# 린팅
flake8 src/ tests/

# 타입 체크 (선택적)
mypy src/
```

## 🔒 보안

### 보안 이슈 리포팅
- 보안 관련 이슈는 public issue로 올리지 말고 이메일로 연락
- 연락처: security [at] anglican [dot] kr

### 보안 가이드라인
- 하드코딩된 비밀번호/토큰 금지
- 환경변수 사용 필수
- 입력 검증 및 새니타이징

## 📋 풀 리퀘스트 체크리스트

- [ ] 모든 테스트 통과
- [ ] 코딩 스타일 준수
- [ ] 문서 업데이트 (필요시)
- [ ] 변경사항 설명 작성
- [ ] 관련 이슈 링크

## 👥 커뮤니티

### 행동 강령
- 서로 존중하고 배려하는 태도
- 건설적인 피드백 제공
- 다양한 의견과 경험 존중

### 소통 채널
- GitHub Issues: 버그 리포트, 기능 제안
- GitHub Discussions: 일반적인 질문, 토론
- 이메일: 보안 이슈, 긴급 문의

## 🏆 기여자 인정

모든 기여자는 다음과 같이 인정받습니다:
- README.md의 Contributors 섹션에 이름 추가
- Release Notes에 기여 내용 명시
- 특별한 기여에 대해서는 별도 감사 표시

감사합니다! 🙏
