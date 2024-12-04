document.addEventListener('DOMContentLoaded', () => {
  const nextBtn = document.getElementById('next-btn');
  const submitBtn = document.querySelector('button[type="submit"]');
  const resultBtn = document.getElementById('result-btn');
  const introScreen = document.getElementById('intro-screen');
  const mainContent = document.getElementById('main-content');
  const secondContent = document.getElementById('second-content');
  const resultContent = document.getElementById('result-content');
  const form = document.querySelector('#user-info-form');  // form element id 수정
  const seasonRadios = document.querySelectorAll('input[name="season"]');
  const styleRadios = document.querySelectorAll('input[name="style"]');
  const heightInput = document.getElementById('height');
  const weightInput = document.getElementById('weight');
  const waistInput = document.getElementById('waist');
  const colorSelect = document.getElementById('color-select');

  // Navigation
  nextBtn.addEventListener('click', () => {
      introScreen.style.display = 'none';
      mainContent.style.display = 'block';
  });

  form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (isFormValid()) {
          mainContent.style.display = 'none';
          secondContent.style.display = 'block';
      } else {
          alert('모든 정보를 올바르게 입력하고 색상을 선택하세요.');
      }
  });

  resultBtn.addEventListener('click', () => {
      if (fitInputsValid()) {
          secondContent.style.display = 'none';
          resultContent.style.display = 'block';
      } else {
          alert('모든 숫자 필드를 올바르게 입력해주세요.');
      }
  });

  // Form Validation
  const isFormValid = () => {
    const seasonChecked = Array.from(seasonRadios).some(radio => radio.checked);
    const styleChecked = Array.from(styleRadios).some(radio => radio.checked);
    const colorValid = colorSelect.value !== ''; // 색상 선택 여부 확인
    const heightValid = heightInput.value !== '' && heightInput.value >= 0 && heightInput.value <= 300;
    const weightValid = weightInput.value !== '' && weightInput.value >= 0 && weightInput.value <= 200;
    const waistValid = waistInput.value !== '' && waistInput.value >= 0 && waistInput.value <= 200;


      return seasonChecked && styleChecked && heightValid && weightValid && waistValid && colorValid;
  };

  const fitInputsValid = () => {
      return (
          heightInput.value !== '' &&
          weightInput.value !== '' &&
          waistInput.value !== '' &&
          !isNaN(heightInput.value) &&
          !isNaN(weightInput.value) &&
          !isNaN(waistInput.value)
      );
  };

  document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault(); // 폼의 기본 제출 기능 막기 (페이지 새로고침 방지)
  
    // 입력 데이터 수집
    const formData = {
        season: document.querySelector('input[name="season"]:checked')?.value,
        style: document.querySelector('input[name="style"]:checked')?.value,
        color: document.getElementById("color-select").value, // 색상 추가
        height: document.getElementById("height").value,
        weight: document.getElementById("weight").value,
        waist: document.getElementById("waist").value,
    };
  
    console.log("수집된 데이터:", formData); // 콘솔에서 확인
  
    // 서버로 데이터 전송 함수 호출
    sendDataToServer(formData);
  });
  
  // 서버로 데이터 전송 함수
  function sendDataToServer(data) {
      fetch('http://localhost:3000/submit', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      })
          .then(response => {
              if (!response.ok) {
                  throw new Error(`HTTP error! status: ${response.status}`);
              }
              return response.text();
          })
          .then(data => {
              console.log('서버 응답:', data);
              alert('데이터가 성공적으로 저장되었습니다.');

              // 성공 시 다음 화면으로 이동
              moveToNextScreen();
          })
          .catch(error => {
              console.error('서버로 데이터 전송 중 오류 발생:', error);
              alert('데이터 전송 중 오류가 발생했습니다.');

              // 오류가 발생하더라도 다음 화면으로 이동
              moveToNextScreen();
          });
  }

  // 다음 화면으로 이동하는 함수
  function moveToNextScreen() {
      document.getElementById('main-content').style.display = 'none'; // 현재 화면 숨김
      document.getElementById('second-content').style.display = 'block'; // 다음 화면 표시
  }


  // 폼 입력 변화 시 제출 버튼 활성화
  form.addEventListener('input', () => {
      const isFormValid = Array.from(seasonInputs).some(input => input.checked) &&
                          Array.from(styleInputs).some(input => input.checked) &&
                          colorSelect.value !== '';
      submitBtn.disabled = !isFormValid;
    });


  // Color Options
  const seasonInputs = document.querySelectorAll('input[name="season"]');
  const styleInputs = document.querySelectorAll('input[name="style"]');
  const colorOptionsDiv = document.getElementById('color-options');

  seasonInputs.forEach(input => input.addEventListener('change', updateColorOptions));
  styleInputs.forEach(input => input.addEventListener('change', updateColorOptions));

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

  function updateColorList(season, style) {
      colorSelect.innerHTML = '<option value="">색상을 선택하세요</option>';

      const colors = {
          '봄': { '캐주얼': ['연두', '핑크'], '스트릿': ['블랙'] },
          '여름': { '아메카지': ['네이비'], '미니멀': ['그레이'] },
          '가을': { '캐주얼': ['갈색', '주황'], '미니멀': ['네이비'] },
          '겨울': { '스트릿': ['화이트', '그레이'], '아메카지': ['카키'] }
      };

      (colors[season]?.[style] || []).forEach(color => {
          const option = document.createElement('option');
          option.value = color;
          option.textContent = color;
          colorSelect.appendChild(option);
      });
  }

  // 전역 함수로 등록
  window.goHome = function goHome() {
      // 초기 화면으로 이동
      location.href = 'index.html'; // index.html 경로를 확인하세요.
  };

});
