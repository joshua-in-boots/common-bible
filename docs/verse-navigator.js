// 검색창에서 입력한 절 번호로 이동
function goToVerse(verseId) {
  const element = document.getElementById(verseId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    // 잠시 하이라이트 효과
    element.style.backgroundColor = '#ffff99';
    setTimeout(() => {
      element.style.backgroundColor = '';
    }, 1500);
  } else {
    alert('해당 절을 찾을 수 없습니다: ' + verseId);
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
  }
});