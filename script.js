document.addEventListener('DOMContentLoaded', () => {
  // 요소 선택
  const submitBtn = document.getElementById('transferButton'); // 전송 버튼
  const form = document.getElementById('user-info-form');      // 폼
  const seasonRadios = document.querySelectorAll('input[name="season"]');
  const styleRadios = document.querySelectorAll('input[name="style"]');
  const heightInput = document.getElementById('height');
  const weightInput = document.getElementById('weight');
  const waistInput = document.getElementById('waist');
  const colorSelect = document.getElementById('color-select');
  const colorOptionsDiv = document.getElementById('color-options');

  // 폼 입력 변화 시 버튼 활성화
  form.addEventListener('input', () => {
    const isValid = checkFormValidity();
    submitBtn.disabled = !isValid; // 버튼 활성화 또는 비활성화
  });

  // 유효성 검사 함수
  function checkFormValidity() {
    const seasonChecked = Array.from(seasonRadios).some(input => input.checked);
    const styleChecked = Array.from(styleRadios).some(input => input.checked);
    const colorValid = colorSelect.value !== '';
    const heightValid = heightInput.value >= 100 && heightInput.value <= 300;
    const weightValid = weightInput.value >= 30 && weightInput.value <= 200;
    const waistValid = waistInput.value >= 30 && waistInput.value <= 200;

    return seasonChecked && styleChecked && colorValid && heightValid && weightValid && waistValid;
  }

  // Color Options 업데이트
  function updateColorOptions() {
    const selectedSeason = document.querySelector('input[name="season"]:checked');
    const selectedStyle = document.querySelector('input[name="style"]:checked');

    if (selectedSeason && selectedStyle) {
      colorOptionsDiv.style.display = 'block';
      updateColorList(selectedSeason.value, selectedStyle.value);
    } else {
      colorOptionsDiv.style.display = 'none';
    }
  }

  // 색상 목록 업데이트
  function updateColorList(season, style) {
    colorSelect.innerHTML = '<option value="">색상을 선택하세요</option>';
    const colors = {
      "봄": { "캐주얼": ["베이지", "화이트"], "스트릿": ["블랙", "네이비"] },
      "여름": { "캐주얼": ["화이트", "네이비"], "스트릿": ["블랙", "그레이"] },
      "가을": { "캐주얼": ["카키", "베이지"], "스트릿": ["블랙", "네이비"] },
      "겨울": { "캐주얼": ["블랙", "그레이"], "스트릿": ["화이트", "블루"] }
    };

    (colors[season]?.[style] || []).forEach(color => {
      const option = document.createElement('option');
      option.value = color;
      option.textContent = color;
      colorSelect.appendChild(option);
    });
  }

  // 시즌과 스타일 변경 시 색상 옵션 업데이트
  seasonRadios.forEach(input => input.addEventListener('change', updateColorOptions));
  styleRadios.forEach(input => input.addEventListener('change', updateColorOptions));

  // 폼 제출 이벤트: 서버로 데이터 전송
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = {
      season: document.querySelector('input[name="season"]:checked')?.value,
      style: document.querySelector('input[name="style"]:checked')?.value,
      color: colorSelect.value,
      height: heightInput.value,
      weight: weightInput.value,
      waist: waistInput.value,
    };

    console.log('수집된 데이터:', formData);

    if (checkFormValidity()) {
      sendDataToServer(formData);
    } else {
      alert('모든 필드를 올바르게 입력해주세요!');
    }
  });

  // 서버로 데이터 전송 함수
  function sendDataToServer(data) {
    fetch('http://localhost:3000/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then(response => {
        if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
        return response.json();
      })
      .then(result => {
        console.log('TempInput 삽입 성공:', result);
        alert('TempInput 데이터가 성공적으로 전송되었습니다!');
  
        fetchGetData()
        fetchDataSequentially()
      })
      .catch(error => {
        console.error('서버로 데이터 전송 중 오류 발생:', error);
        alert('서버와 통신 중 문제가 발생했습니다.');
      });
  }
  
  function fetchGetData() {
    fetch('http://localhost:3000/get-data')
      .then(response => {
        if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
        return response.json();
      })
      .then(data => {
        console.log('TempInput 데이터:', data);
        alert('TempInput 데이터 조회 완료!');
      })
      .catch(error => {
        console.error('데이터 조회 중 오류 발생:', error);
        alert('데이터 조회 중 문제가 발생했습니다.');
      });
  }
  

  // 연속 데이터 호출 함수
  function fetchDataSequentially() {
    fetch('http://localhost:3000/get-waist')
      .then(response => response.json())
      .then(data => {
        console.log('허리 정보:', data);
        return fetch('http://localhost:3000/get-size-info');
      })
      .then(response => response.json())
      .then(data => {
        console.log('사이즈 정보:', data);
        return fetch('http://localhost:3000/get-outfit-recommendations');
      })
      .then(response => response.json())
      .then(data => {
        console.log('추천 의상:', data);
        return fetch('http://localhost:3000/get-color-matching');
      })
      .then(response => response.json())
      .then(data => {
        console.log('색상 매칭:', data);
        alert('모든 데이터가 성공적으로 가져와졌습니다!');
      })
      .catch(error => {
        console.error('데이터 연속 호출 중 오류 발생:', error);
      });
      
  }
});
