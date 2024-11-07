let currentPage = 1;
const itemsPerPage = 10;
let currentCategory = null;
let allItems = []; // 모든 상품 데이터를 저장할 변수

// 상품 데이터를 불러와 필터링하는 함수
function loadItems() {
  return fetch("/static/products_data.json")  // JSON 파일 경로 확인
    .then(response => response.json())  // JSON 데이터로 변환
    .then(data => {
      console.log("Data fetched successfully:", data); // 데이터 확인용 로그
      return data.items;  // "items" 배열 반환
    });
}

// 카테고리에 따라 필터링된 상품을 불러오는 함수
function loadProducts(category = null) {
  if (allItems.length === 0) {
    // 최초 로드 시에만 데이터를 불러옴
    loadItems().then((items) => {
      allItems = items; // 전체 데이터를 저장
      console.log("All items loaded:", allItems); // 데이터 확인용 로그
      currentCategory = category;
      displayFilteredItems();
    }).catch(error => console.error("Error loading products:", error));
  } else {
    currentCategory = category;
    currentPage = 1; // 페이지를 1로 초기화
    displayFilteredItems();
  }
}

// 필터링 및 페이지네이션 적용하여 상품을 표시하는 함수
function displayFilteredItems() {
  const filteredItems = currentCategory ? allItems.filter(item => item.category === currentCategory) : allItems;
  console.log("Filtered items:", filteredItems); // 필터링된 데이터 확인용 로그
  displayItems(filteredItems, currentPage);
}

// 상품들을 화면에 표시하는 함수
function displayItems(items, page) {
  const startIndex = (page - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const itemsToDisplay = items.slice(startIndex, endIndex);

  const productGrid = document.getElementById('products');
  if (!productGrid) {
    console.error("Element with id 'products' not found.");
    return;
  }
  
  productGrid.innerHTML = ''; // 기존 상품 목록 초기화

  if (itemsToDisplay.length === 0) {
    console.warn("No items to display on this page.");
  }

  itemsToDisplay.forEach(item => {
    const productItem = document.createElement('div');
    productItem.classList.add('product-item');
    productItem.innerHTML = `
      <a href="/product-detail.html?id=${item.id}">
        <img src="/${item.imageUrl}" alt="${item.title}">
        <div class="title" data-title="${item.title}">${item.title}</div>
        <div class="date">${item.date}</div>
      </a>
    `;
    productGrid.appendChild(productItem);
  });

  // 페이지네이션 표시 함수 호출
  displayPagination(items);
}

// 페이지네이션 버튼 생성 함수
function displayPagination(items) {
  const pagination = document.getElementById('pagination');
  if (!pagination) {
    console.error("Element with id 'pagination' not found.");
    return;
  }

  pagination.innerHTML = ''; // 기존 페이지네이션 초기화

  const totalPages = Math.ceil(items.length / itemsPerPage);

  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement('button');
    pageButton.innerText = i;
    pageButton.classList.add('page-btn');

    // 현재 페이지 스타일 추가
    if (i === currentPage) {
      pageButton.classList.add('active');
    }

    // 버튼 클릭 시 해당 페이지로 이동
    pageButton.addEventListener('click', () => {
      currentPage = i;
      displayItems(items, currentPage); // 기존 데이터를 사용하여 페이지 변경
    });

    pagination.appendChild(pageButton);
  }
}

// 페이지가 로드될 때 전체 상품을 1페이지부터 출력
document.addEventListener('DOMContentLoaded', () => {
  loadProducts(); // 기본적으로 모든 상품을 표시
});



/*상세페이지 관련 코드*/

// URL 쿼리 파라미터에서 상품 ID 가져오기
const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get('id'); // id 파라미터 값

// 상품 데이터를 불러와서 상세 페이지에 표시하는 함수
function loadProductDetail(productId) {
  fetch('/static/products_data.json')
      .then(response => response.json())
      .then(data => {
          const product = data.items.find(item => item.id == productId); // 해당 ID의 상품 찾기

          if (product) {
              document.getElementById('product-detail').innerHTML = `
                  <h1>${product.title}</h1>
                  <img src="/${product.imageUrl}" alt="${product.title}">
                  <p><strong>날짜:</strong> ${product.date}</p>
                  <p><strong>카테고리:</strong> ${product.category}</p>
                  <p><strong>상세 설명:</strong> ${product.description}</p>
              `;
          } else {
              document.getElementById('product-detail').innerHTML = `<p>상품을 찾을 수 없습니다.</p>`;
          }
      })
      .catch(error => console.error("상품 상세 정보 불러오기 오류:", error));
}

// 페이지가 로드될 때 상품 상세 정보 로드
if (productId) {
  loadProductDetail(productId);
} else {
  document.getElementById('product-detail').innerHTML = `<p>상품 ID가 잘못되었습니다.</p>`;
}
