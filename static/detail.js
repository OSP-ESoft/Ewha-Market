// Firebase 초기화 설정 (기존 설정 사용)
import { getDatabase, ref, child, get } from "firebase/database";

document.getElementById("buy_btn").addEventListener("click", function () {
    const sellerId = this.getAttribute("data-seller-id"); // 판매자 ID 가져오기
    const dbRef = ref(getDatabase());

    // Firebase에서 판매자 정보 가져오기
    get(child(dbRef, `users/${sellerId}`))
        .then((snapshot) => {
            if (snapshot.exists()) {
                const sellerData = snapshot.val();
                const phone = sellerData.phone || "전화번호 없음";
                const email = sellerData.email || "이메일 없음";

                // 팝업 생성
                alert(`판매자 정보\n전화번호: ${phone}\n이메일: ${email}`);
            } else {
                alert("판매자 정보를 찾을 수 없습니다.");
            }
        })
        .catch((error) => {
            console.error("Error fetching seller data:", error);
            alert("판매자 정보를 가져오는 중 오류가 발생했습니다.");
        });
});
