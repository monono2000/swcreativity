document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소들
    const nextBtn = document.getElementById('next-btn');  // 'Next' 버튼 (사용자 정보 페이지로 이동)
  
    // 'Next' 버튼 클릭 시 사용자 정보 입력 페이지로 이동
    nextBtn.addEventListener('click', () => {
      window.location.href = 'index.html';  // 사용자 정보 페이지로 이동
    });
  
    
    const seasonInputs = document.querySelectorAll('input[name="season"]');
    const styleInputs = document.querySelectorAll('input[name="style"]');
    const colorOptionsDiv = document.getElementById('color-options');
    const colorSelect = document.getElementById('color-select');
  
    // 시즌과 스타일에 따라 색상 옵션 업데이트
    function updateColorOptions() {
      const selectedSeason = document.querySelector('input[name="season"]:checked');
      const selectedStyle = document.querySelector('input[name="style"]:checked');
      if (selectedSeason && selectedStyle) {
        colorOptionsDiv.style.display = 'block'; // 컬러 선택 영역 보이기
        updateColorList(selectedSeason.value, selectedStyle.value);
      } else {
        colorOptionsDiv.style.display = 'none'; // 컬러 선택 영역 숨기기
      }
    }
  
    // 색상 목록 업데이트
    function updateColorList(season, style) {
      const colors = {
        '봄': { '캐주얼': ['연두', '핑크'], '스트릿': ['블랙'] },
        '여름': { '아메카지': ['네이비'], '미니멀': ['그레이'] },
        '가을': { '캐주얼': ['갈색', '주황'], '미니멀': ['네이비'] },
        '겨울': { '스트릿': ['화이트', '그레이'], '아메카지': ['카키'] },
      };
  
      // 컬러 선택 초기화
      colorSelect.innerHTML = '<option value="">색상을 선택하세요</option>';
  
      // 선택된 시즌과 스타일에 따른 색상 추가
      (colors[season]?.[style] || []).forEach(color => {
        const option = document.createElement('option');
        option.value = color;
        option.textContent = color;
        colorSelect.appendChild(option);
      });
    }
  
    // 이벤트 리스너 추가
    seasonInputs.forEach(input => input.addEventListener('change', updateColorOptions));
    styleInputs.forEach(input => input.addEventListener('change', updateColorOptions));
  
    // "다음" 버튼 클릭 시 알림창 띄우기 및 페이지 이동
    submitBtn.addEventListener('click', () => {
      window.location.href = 'result.html';
    });
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  });
  