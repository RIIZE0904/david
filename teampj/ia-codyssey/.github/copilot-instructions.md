# Copilot Instructions for ia-codyssey

## 프로젝트 개요
- 이 저장소는 Python 기반 실습 및 웹 프레임워크(Flask) 예제, 계산기 기능 구현 등 교육 목적의 코드가 포함되어 있습니다.
- 주요 폴더: `course1/question1`, `course1/question2`, `course1/question3/david`
- 주요 파일: `app.py`(Flask 웹앱), `calculator.py`(콘솔 계산기)

## 아키텍처 및 주요 컴포넌트
- `app.py`: Flask 웹 서버. `/` 엔드포인트에서 gTTS로 생성한 음성(mp3)을 반환.
  - 외부에서 접근 가능하도록 `0.0.0.0`으로 호스트 지정.
  - gTTS 패키지로 텍스트를 음성으로 변환.
- `calculator.py`: 콘솔 기반 계산기. 두 가지 모드 지원:
  - 숫자 입력 방식: 두 숫자와 연산자 입력
  - 문자열 수식 입력 방식: "숫자 연산자 숫자" 형태의 한 줄 입력
  - 예외 처리(잘못된 입력, 0으로 나누기 등) 포함

## 개발 환경 및 워크플로우
- Python 가상환경(venv) 사용 권장: `python3 -m venv venv` → `source venv/bin/activate`
- 패키지 설치: `pip install flask gtts`
- Flask 서버 실행: `python app.py` 또는 VS Code에서 "Run Without Debugging"
- 계산기 실행: `python calculator.py`
- VS Code에서 Python 인터프리터를 반드시 venv로 선택해야 함

## 프로젝트별 관례 및 패턴
- 함수명은 영어 소문자, 언더스코어 사용
- 예외 발생 시 사용자 친화적 메시지 출력
- Flask 앱은 `if __name__ == '__main__':`에서 실행
- gTTS 사용 시 인자 명시적 지정 권장: `gTTS(text, lang=lang, tld="com")`
- 계산기 기능은 입력값 검증 및 예외 처리 필수

## 통합 및 외부 의존성
- 외부 패키지: Flask, gTTS
- gTTS는 `BytesIO`를 활용해 파일 저장 없이 음성 데이터를 반환
- Flask는 GET 요청 파라미터로 언어 선택 가능

## 예시 코드 패턴
```python
# Flask 음성 반환 예시
@app.route("/")
def home():
    text = "Hello, DevOps"
    lang = request.args.get('lang', 'ko')
    fp = BytesIO()
    gTTS(text, lang=lang, tld="com").write_to_fp(fp)
    fp.seek(0)
    return Response(fp.getvalue(), mimetype='audio/mpeg')
```

```python
# 계산기 수식 입력 예시
expr = input("Enter expression: ")
parts = expr.strip().split()
if len(parts) == 3:
    num1, operator, num2 = parts
    # ... 연산 및 예외 처리 ...
```

## 기타
- README.md, assignment.md에 개발 환경 및 Flask 개념 정리 있음
- 추가 규칙이나 관례 발견 시 이 파일에 업데이트
