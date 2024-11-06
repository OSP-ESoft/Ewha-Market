function loadProducts(category) {
    fetch('/products.json') 
      .then(response => response.json())
      .then(data => {
        if (!Array.isArray(data)) {
          throw new Error("Data is not an array");
        }
        // 선택한 카테고리에 맞는 상품만 필터링
        const filteredProducts = data.filter(product => product.category === category);
        
        const productList = document.getElementById('products');
        productList.innerHTML = ''; // 기존 목록 지우기
  
        // 필터링된 상품을 목록에 추가
        filteredProducts.forEach(product => {
          const listItem = document.createElement('li');
          listItem.classList.add('product_item'); //스타일링 위한 클래스
          listItem.innerHTML = `
            <img src="${product.imageUrl}" alt="${product.title}">
            <h3>${product.title}</h3>
            // <p>등록일: ${product.date}</p>
          `;
          productList.appendChild(listItem);
        });
      })
      .catch(error => console.error('Error loading products:', error));
  }