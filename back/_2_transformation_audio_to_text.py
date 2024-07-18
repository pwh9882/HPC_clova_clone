from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import os
import requests

@socketio.on('process_audio')
def handle_audio_data():
    try:
        # 음성 파일을 텍스트로 변환
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print("Recognized Text: ", text)

            # LLM 서버로 텍스트 전송 및 요약본 수신
            summary = get_summary_from_llm(text)
            print("Summary: ", summary)

            # 변환된 텍스트와 요약본을 클라이언트로 전송
            emit('text_data', {'text': text, 'summary': summary})

        # 임시 파일 삭제
        os.remove("temp_audio.wav")

    except Exception as e:
        print("오디오 인식 오류 : ", str(e))
        emit('text_data', {'text': '오디오 인식 오류', 'summary': ''})
