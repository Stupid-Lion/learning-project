import os
from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import random
import string
import time
import threading

app = Flask(__name__)

# 언어 매핑 딕셔너리 정의
lang_mapping = {
    '영어': 'en',
    '한국어': 'ko',
    '일본어': 'ja',
    '스페인어': 'es',
    '프랑스어': 'fr',
    '독일어': 'de',
    '중국어': 'zh-CN'
}

# static 폴더 확인 및 생성
static_folder = os.path.join(os.getcwd(), 'static')
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    lang = request.form['lang']
    
    # 언어 매핑을 이용하여 번역 대상 언어 설정
    dest_lang = lang_mapping.get(lang, 'en')
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang, src='auto')
    return jsonify({'translated_text': translated.text})

@app.route('/tts', methods=['POST'])
def tts():
    text = request.form['translated_text']  # 번역된 텍스트 받기
    lang = request.form['lang']
    
    # 음성 변환 언어 설정
    dest_lang = lang_mapping.get(lang, 'en')
    
    # 고유한 음성 파일 이름 생성 (타임스탬프나 랜덤 문자열 사용)
    unique_filename = 'translated_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.mp3'
    save_path = os.path.join(static_folder, unique_filename)  # 동적 파일 경로 생성

    # 음성 파일 생성
    tts = gTTS(text=text, lang=dest_lang)
    tts.save(save_path)  # 번역된 텍스트로 음성 파일 생성 및 저장

    # 음성 파일 경로를 반환 (동적으로 생성된 파일 경로 사용)
    audio_file_path = f'/static/{unique_filename}'
    print(f"Generated audio file path: {audio_file_path}")  # 경로 확인을 위한 로그 출력

    # 음성 파일 삭제를 위한 1분 후 삭제 처리
    def delete_audio_file():
        time.sleep(60)  # 1분 후 삭제
        if os.path.exists(save_path):
            os.remove(save_path)  # 파일 삭제
            print(f"File {save_path} deleted.")

    # 파일 삭제를 위한 쓰레드 시작
    threading.Thread(target=delete_audio_file).start()

    return jsonify({'audio_file': audio_file_path})  # 동적 파일 경로 반환

if __name__ == "__main__":
    app.run(debug=True)
