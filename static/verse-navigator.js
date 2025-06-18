// 성경 책 이름 매핑 데이터 (bible_book_mappings.json과 동기화)
const BOOK_MAPPINGS = {
  '창세기': '창세', '출애굽기': '출애', '레위기': '레위', '민수기': '민수', '신명기': '신명',
  '여호수아': '여호', '판관기': '판관', '룻기': '룻기', 
  '사무엘상': '1사무', '사무엘하': '2사무',
  '열왕기상': '1열왕', '열왕기하': '2열왕',
  '역대기상': '1역대', '역대기하': '2역대',
  '에즈라': '에즈', '느헤미야': '느헤', '토비트': '토비', '유딧': '유딧', '에스델': '에스',
  '마카베오상': '1마카', '마카베오하': '2마카',
  '욥기': '욥기', '시편': '시편', '잠언': '잠언', '전도서': '전도', '아가': '아가',
  '지혜서': '지혜', '집회서': '집회',
  '이사야': '이사', '예레미야': '예레', '애가': '애가', '바룩': '바룩', '에제키엘': '에제', '다니엘': '다니',
  '호세아': '호세', '요엘': '요엘', '아모스': '아모', '오바디야': '오바', '요나': '요나', '미가': '미가',
  '나훔': '나훔', '하바꾹': '하바', '스바니야': '스바', '하깨': '하깨', '즈가리야': '즈가', '말라기': '말라',
  '마태오의 복음서': '마태', '마르코의 복음서': '마르', '루가의 복음서': '루가', '요한의 복음서': '요한',
  '사도행전': '사도',
  '로마인들에게 보낸 편지': '로마',
  '고린토인들에게 보낸 첫째 편지': '1고린', '고린토인들에게 보낸 둘째 편지': '2고린',
  '갈라디아인들에게 보낸 편지': '갈라', '에페소인들에게 보낸 편지': '에페',
  '필립비인들에게 보낸 편지': '필립', '골로사이인들에게 보낸 편지': '골로',
  '데살로니카인들에게 보낸 첫째 편지': '1데살', '데살로니카인들에게 보낸 둘째 편지': '2데살',
  '디모테오에게 보낸 첫째 편지': '1디모', '디모테오에게 보낸 둘째 편지': '2디모',
  '디도에게 보낸 편지': '디도', '필레몬에게 보낸 편지': '필레',
  '히브리인들에게 보낸 편지': '히브', '야고보의 편지': '야고',
  '베드로의 첫째 편지': '1베드', '베드로의 둘째 편지': '2베드',
  '요한의 첫째 편지': '1요한', '요한의 둘째 편지': '2요한', '요한의 셋째 편지': '3요한',
  '유다의 편지': '유다', '요한의 묵시록': '묵시'
};

// 입력된 텍스트를 절 ID로 변환
function parseSearchInput(input) {
  input = input.trim();
  
  // 1. 이미 절 ID 형식인 경우 (예: "창세-1-3")
  if (input.match(/^[가-힣]+-\d+-\d+[a-z]?$/)) {
    return [input];
  }
  
  // 2. "창세기 1:3" 또는 "창세 1:3" 형식 처리
  const bookChapterVerseMatch = input.match(/^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$/);
  if (bookChapterVerseMatch) {
    const [, bookName, chapter, startVerse, endVerse] = bookChapterVerseMatch;
    
    // 책 이름을 약칭으로 변환
    const shortName = BOOK_MAPPINGS[bookName] || bookName;
    
    if (endVerse) {
      // 범위 검색 (예: "창세 1:1-3")
      const results = [];
      for (let verse = parseInt(startVerse); verse <= parseInt(endVerse); verse++) {
        results.push(`${shortName}-${chapter}-${verse}`);
      }
      return results;
    } else {
      // 단일 절 (예: "창세 1:3")
      return [`${shortName}-${chapter}-${startVerse}`];
    }
  }
  
  // 3. 다른 형식은 그대로 반환
  return [input];
}

// 검색창에서 입력한 절 번호로 이동 (다중 절 지원)
function goToVerse(searchInput) {
  const verseIds = parseSearchInput(searchInput);
  let foundAny = false;
  
  // 이전 하이라이트 제거
  document.querySelectorAll('.highlighted-verse').forEach(el => {
    el.classList.remove('highlighted-verse');
    el.style.backgroundColor = '';
  });
  
  verseIds.forEach((verseId, index) => {
    const element = document.getElementById(verseId);
    if (element) {
      foundAny = true;
      
      // 첫 번째 절로 스크롤
      if (index === 0) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      
      // 하이라이트 효과
      element.classList.add('highlighted-verse');
      element.style.backgroundColor = '#ffff99';
    }
  });
  
  if (!foundAny) {
    alert('해당 절을 찾을 수 없습니다: ' + searchInput);
  } else {
    // 3초 후 하이라이트 제거
    setTimeout(() => {
      document.querySelectorAll('.highlighted-verse').forEach(el => {
        el.style.backgroundColor = '';
        el.classList.remove('highlighted-verse');
      });
    }, 3000);
  }
}

// 예시: URL에 #창세-1-3 이 있으면 자동 이동
window.addEventListener('DOMContentLoaded', () => {
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    goToVerse(hash);
  }

  // 검색 박스 이벤트 바인딩
  const searchBox = document.getElementById('verse-search');
  const searchBtn = document.getElementById('verse-search-btn');

  if (searchBox && searchBtn) {
    searchBtn.addEventListener('click', () => {
      const value = searchBox.value.trim();
      if (value) goToVerse(value);
    });

    searchBox.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const value = searchBox.value.trim();
        if (value) goToVerse(value);
      }
    });
    
    // 검색 예시를 placeholder에 표시
    if (searchBox) {
      searchBox.placeholder = "예: 창세-1-3, 창세기 1:3, 창세 1:1-3";
    }
  }
});
