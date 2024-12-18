document.addEventListener('DOMContentLoaded', () => {
    // 전역 함수로 등록
    window.goHome = function goHome() {
        // 초기 화면으로 이동
        location.href = 'start.html'; // index.html 경로를 확인하세요.
    };

    // 초기 제품 배열
    const products = [
        { name: '상품 1', image: 'recommend_images_output/rec1.png', brand: '브랜드 1', price: '₩50,000', discount: '20%' },
        { name: '상품 2', image: 'recommend_images_output/rec2.png', brand: '브랜드 2', price: '₩60,000', discount: '15%' },
        { name: '상품 3', image: 'recommend_images_output/rec3.png', brand: '브랜드 3', price: '₩70,000', discount: '10%' }
    ];    

    // CSV 파일을 불러오고 id, image, name, brand, price, discount 값을 업데이트하는 함수
    function loadProductIdsFromCSV() {
        const csvFilePath = 'recommend2.csv'; // CSV 파일 경로

        // PapaParse로 CSV를 파싱
        Papa.parse(csvFilePath, {
            download: true,  // 파일을 다운로드
            header: true,    // CSV 파일에 헤더가 있을 경우
            dynamicTyping: true, // 숫자와 불리언 자동 변환
            complete: function(results) {
                const csvData = results.data;

                // CSV 데이터를 사용하여 각 상품의 데이터를 업데이트
                products.forEach((product, index) => {
                    if (csvData[index]) {
                        product.id = csvData[index]['링크번호'];  // 'Old File Name' 열을 id로 사용
                        product.image = csvData[index]['Tag'];  // 'New File Name' 열을 image로 사용
                        product.name = csvData[index]['상품명'];
                        product.brand = csvData[index]['브랜드'];
                        product.price = csvData[index]['가격'];
                        product.discount = csvData[index]['할인율']; // 할인율 추가
                    }
                });

                // 상품 정보를 페이지에 업데이트
                loadProducts();
            },
            error: function(error) {
                console.error("CSV 파일을 로드하는 중 오류가 발생했습니다:", error);
            }
        });
    }

    // 각 상품을 동적으로 할당하는 함수
    function loadProducts() {
        products.forEach((product, index) => {
            // 상품 링크 및 이미지 업데이트
            document.getElementById(`product-link-${index}`).href = `https://www.musinsa.com/products/${product.id}`;
            document.getElementById(`product-image-${index}`).src = `recommend_images_output/reco${product.image}.png`;

            // 상품명, 브랜드명 업데이트
            document.getElementById(`product-name-${index}`).innerText = product.name;
            document.getElementById(`product-brand-${index}`).innerText = product.brand;

            // 가격 및 할인율 업데이트
            const priceElement = document.getElementById(`product-price-${index}`);
            priceElement.innerText = product.price;

            // 할인율을 가격 옆에 추가
            if (product.discount) { // 할인율이 존재할 경우에만 추가
                const discountElement = document.createElement('span'); // 새로운 <span> 태그 생성
                discountElement.className = 'product-discount';         // 클래스 이름 추가 (CSS 스타일링 가능)
                discountElement.innerText = ` (${product.discount})`;   // 할인율 추가
                priceElement.appendChild(discountElement);              // 가격 옆에 추가
            }
        });
    }

    
    // 페이지 로드 시 상품 정보 동적 할당
    window.onload = loadProductIdsFromCSV;
});
