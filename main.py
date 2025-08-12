<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔮 사주 & 연애운 테스트</title>
<style>
    body {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        background-color: #fff8f8;
        text-align: center;
        padding: 20px;
    }
    h1 {
        color: #ff6699;
        margin-bottom: 10px;
    }
    .container {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        max-width: 400px;
        margin: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    input[type="date"], select {
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #ff99bb;
        font-size: 16px;
        margin-top: 10px;
        width: 80%;
    }
    button {
        margin-top: 15px;
        padding: 10px 20px;
        background: #ff99bb;
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    button:hover {
        background: #ff6699;
    }
    .result {
        margin-top: 20px;
        padding: 15px;
        background: #fff0f5;
        border-radius: 10px;
        font-size: 16px;
        color: #555;
    }
</style>
</head>
<body>

<h1>🔮 사주 & 연애운 테스트</h1>
<div class="container">
    <label for="birth">생년월일</label><br>
    <input type="date" id="birth"><br><br>

    <label for="type">궁금한 운세</label><br>
    <select id="type">
        <option value="saju">사주</option>
        <option value="love">연애운</option>
    </select><br>

    <button onclick="checkFortune()">운세 확인하기</button>

    <div class="result" id="result"></div>
</div>

<script>
function checkFortune() {
    const birth = document.getElementById('birth').value;
    const type = document.getElementById('type').value;
    const resultDiv = document.getElementById('result');

    if (!birth) {
        resultDiv.innerHTML = "📅 생년월일을 입력해주세요!";
        return;
    }

    let message = "";
    if (type === "saju") {
        message = "🧧 오늘은 사주가 평온하고 안정적인 하루가 될 것 같아요. 중요한 결정을 내리기에 좋은 날입니다!";
    } else if (type === "love") {
        message = "💖 오늘은 사랑의 기운이 가득해요! 새로운 인연이 다가올 수 있으니 주변을 잘 살펴보세요.";
    }

    resultDiv.innerHTML = `
        <strong>🎂 생년월일:</strong> ${birth}<br>
        <strong>🔮 결과:</strong> ${message}
    `;
}
</script>

</body>
</html>
