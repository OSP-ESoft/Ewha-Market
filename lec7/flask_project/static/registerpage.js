// script.js 파일에 추가할 JavaScript 코드

document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById("signupForm");
    const checkUsernameButton = document.getElementById("checkUsername");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const usernameMessage = document.getElementById("usernameMessage");
    const passwordMessage = document.getElementById("passwordMessage");

    // 예시 데이터베이스의 중복된 아이디 리스트
    const existingUsernames = ["user1", "testuser", "example"];

    // 아이디 중복 확인 버튼 클릭 시 이벤트 처리
    checkUsernameButton.addEventListener("click", function() {
        const username = usernameInput.value.trim();

        if (username === "") {
            usernameMessage.textContent = "아이디를 입력해주세요.";
            usernameMessage.style.color = "red";
        } else if (existingUsernames.includes(username)) {
            usernameMessage.textContent = "이미 사용 중인 아이디입니다.";
            usernameMessage.style.color = "red";
        } else {
            usernameMessage.textContent = "사용 가능한 아이디입니다.";
            usernameMessage.style.color = "green";
        }
    });

    // 비밀번호 일치 여부 확인
    confirmPasswordInput.addEventListener("input", function() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (password !== confirmPassword) {
            passwordMessage.textContent = "비밀번호가 일치하지 않습니다.";
            passwordMessage.style.color = "red";
        } else {
            passwordMessage.textContent = "";
        }
    });

    // 폼 제출 시 유효성 검사
    signupForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // 아이디 중복 확인
        if (existingUsernames.includes(username)) {
            alert("이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.");
            return;
        }

        // 비밀번호 규칙 확인 (영문, 숫자 포함 8~16자)
        const passwordPattern = /^(?=.*[a-zA-Z])(?=.*\d).{8,16}$/;
        if (!passwordPattern.test(password)) {
            alert("비밀번호는 영문, 숫자를 포함하여 8~16자로 설정해주세요.");
            return;
        }

        // 비밀번호 재확인 일치 여부 확인
        if (password !== confirmPassword) {
            alert("비밀번호가 일치하지 않습니다. 다시 확인해주세요.");
            return;
        }

        // 모든 조건을 만족하면 회원가입 페이지로 이동
        alert("회원가입이 완료되었습니다!");
        window.location.href = "/register";
    });
});
