body { 
    font-family: 'Arial', sans-serif;
    background-color: #f9f9f9;
    margin: 0;
    padding: 20px;
}

/* 네비게이션 바 스타일 */
.navbar {
    background-color: #00462A;
    padding: 20px;
    display: flex;
    justify-content: center; /* 중앙 정렬 */
    align-items: center;
    position: relative;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.navbar__logo {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}

.navbar__logo a {
    color: white;
    text-decoration: none;
    font-size: 32px; /* 로고 크기 확대 */
    font-weight: bold;
}

.navbar__menu {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 30px; /* 메뉴 간격을 더 넓게 설정 */
}

.navbar__menu li {
    display: inline-block;
}

.menu {
    color: white;
    padding: 10px 20px;
    font-size: 18px;
    text-decoration: none;
}

.menu:hover, .menu.active {
    text-decoration: underline;
}

/* 로그인 버튼 우측 배치 */
.login_button {
    position: absolute;
    right: 50px;
}

.login_button ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 20px; /* 로그인 버튼 간격 설정 */
}

.login_bar li {
    display: inline-block;
}

.login_menu {
    color: white;
    font-size: 18px;
    text-decoration: none;
    padding: 10px 20px;
}

.login_menu:hover {
    text-decoration: underline;
}

/* 리뷰 작성 페이지 스타일 */
.container {
    max-width: 800px;
    margin: 40px auto;
    background-color: #ffffff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
}

h1, h2 {
    text-align: center;
    color: #006937; 
}

.form-group {
    margin-bottom: 20px;
}

label {
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
}

input[type="text"], input[type="file"], textarea, select {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

textarea {
    height: 100px;
}

button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    opacity: 0.9;
}

.submit-btn {
    background-color: #28a745;
    color: white;
}

.cancel-btn {
    background-color: #dc3545;
    color: white;
}

.rating-section {
    display: flex;
    align-items: center;
}

.rating {
    display: flex;
    gap: 5px;
    margin-right: 10px;
}

.star {
    font-size: 24px;
    color: #ccc;
    cursor: pointer;
}

.star.selected {
    color: #006400;
}

.file-buttons {
    display: flex;
    gap: 10px;
}

.file-buttons button {
    background-color: #006400;
    color: white;
}

.file-upload-section #file-name {
    display: block;
    margin-top: 10px;
}

.buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
