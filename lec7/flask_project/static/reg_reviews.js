document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star");
    const ratingText = document.getElementById("rating-text");
    const reviewForm = document.getElementById("reviewForm");
    const loginLogoutButton = document.getElementById('loginLogoutButton');

    // 별점 선택 로직
    stars.forEach(star => {
        star.addEventListener("click", () => {
            const value = star.getAttribute("data-value");

            // 모든 별점에서 'selected' 클래스 제거
            stars.forEach(s => s.classList.remove("selected"));

            // 선택된 별점만큼 'selected' 클래스 추가
            for (let i = 0; i < value; i++) {
                stars[i].classList.add("selected");
            }

            // 선택된 별점 표시
            ratingText.textContent = `${value}점 선택됨`;
        });
    });

    // 네비게이션 바에서 로그아웃 처리
    if (loginLogoutButton && loginLogoutButton.textContent.trim() === "로그아웃") {
        loginLogoutButton.addEventListener('click', (event) => {
            event.preventDefault();  // 기본 동작 방지

            // 로그아웃 요청을 비동기적으로 서버에 전송
            fetch('/logout', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        // 로그아웃 후 버튼을 '로그인'으로 변경하고 로그인 페이지로 이동
                        loginLogoutButton.textContent = '로그인';
                        loginLogoutButton.href = '/loginpage';
                        window.location.href = '/loginpage';  // 로그인 페이지로 리다이렉트
                    } else {
                        console.error('로그아웃 실패');
                    }
                })
                .catch(error => console.error('Error occurred during logout:', error));
        });
    }
});

// 파일 이름 표시
function showFileName() {
    const fileInput = document.getElementById('file');
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        document.getElementById('file-name').textContent = `Review Image upload : ${fileName}`;
    }
}

// 리뷰 작성 취소 시 폼 초기화
function cancelReview() {
    const reviewForm = document.getElementById("reviewForm");
    reviewForm.reset();
    document.getElementById('file-name').textContent = 'Review Image upload : ';
    document.getElementById("rating-text").textContent = "별점을 선택해주세요.";

    // 별점 초기화
    const stars = document.querySelectorAll(".star");
    stars.forEach(star => star.classList.remove("selected"));
}
