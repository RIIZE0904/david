from flask import Flask, request, render_template
import os
from io import BytesIO
from gtts import gTTS
import base64

DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko')
LANG_OPTIONS = ['ko', 'en', 'ja', 'es','error']

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize variables
    # error handling and audio generation
    error = None
    audio_b64 = None
    # Default text and language
    text = ''
    lang = DEFAULT_LANG


    if request.method == "POST":
        text = request.form.get("input_text", "").strip()
        lang = request.form.get("lang", DEFAULT_LANG)
        if not text:
            error = "텍스트를 입력하세요."
        elif lang not in LANG_OPTIONS:
            error = "지원하지 않는 언어입니다."
        else:
            try:
                fp = BytesIO()
                gTTS(text, lang=lang, tld="com").write_to_fp(fp)
                fp.seek(0)
                audio_b64 = base64.b64encode(fp.getvalue()).decode('utf-8')
                # 입력 내역 로그 저장
                with open("input_log.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"{text}\t{lang}\n")
            except Exception as e:
                error = f"TTS 변환 실패: {e}"

    # mp3 다운로드 링크 생성 (base64 데이터가 있을 때만)
    mp3_download_url = None
    if audio_b64:
        mp3_download_url = f"data:audio/mpeg;base64,{audio_b64}"

    return render_template(
        "index.html",
        error=error,
        audio=audio_b64,
        mp3_download_url=mp3_download_url
    )

if __name__ == '__main__':
    app.run('0.0.0.0', 80)