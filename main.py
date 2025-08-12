from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>🔮 사주 & 연애운 테스트</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            background: #f0e6f6;
            color: #333;
            padding: 2rem;
            max-width: 600px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #6a0dad;
        }
        label {
            display: block;
            margin-top: 1rem;
            font-weight: bold;
        }
        input[type="date"], select {
            width: 100%;
            padding: 0.5rem;
            margin-top: 0.3rem;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            margin-top: 1.5rem;
            width: 100%;
            padding: 0.7rem;
            border: none;
            border-radius: 5px;
            background-color: #6a0dad;
            color: white;
            font-size: 1.1rem;
            cursor: pointer;
        }
        button:hover {
            background-color: #580aab;
        }
        .result {
            margin-top: 2rem;
            padding: 1rem;
            background: #e6d7f5;
            border-radius: 8px;
            font-size: 1.1rem;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>🔮 사주 & 연애운 테스트</h1>
    <form method="POST">
        <label for="birthdate">생년월일 입력:</label>
        <input type="date" id="birthdate" name="birthdate" required />
        
        <label for="testtype">테스트 유형 선택:</label>
        <select id="testtype" name="testtype" required>
            <option value="saju">사주</option>
            <option value="love">연애운</option>
        </select>
        
        <button type="submit">결과 보기</button>
    </form>

    {% if result %}
    <div class="result">
        {{ result }}
    </div>
    {% endif %}
</body>
</html>
"""

def 사주_테스트(birthdate):
    # 실제 사주 분석 대신 예시 텍스트 반환
    return f"{birthdate} 출생자분의 사주 운세는 매우 긍정적입니다! 앞으로 좋은 일이 많을 거예요."

def 연애운_테스트(birthdate):
    # 실제 연애운 분석 대신 예시 텍스트 반환
    return f"{birthdate} 출생자분의 오늘 연애운은 별 5개 만점 중 4개입니다! 좋은 인연이 다가올 수 있어요."

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        birthdate = request.form.get("birthdate")
        testtype = request.form.get("testtype")
        if birthdate and testtype:
            if testtype == "saju":
                result = 사주_테스트(birthdate)
            elif testtype == "love":
                result = 연애운_테스트(birthdate)
    return render_template_string(HTML_PAGE, result=result)

if __name__ == "__main__":
    app.run(debug=True)
