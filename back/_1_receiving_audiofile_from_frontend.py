'''
frontend로부터 audio 파일 수신
파일 업로드 endpoint 구현은 '/upload'로 하였음
'''
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

recognizer = sr.Recognizer()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}) # Python 객체 -> JSON 응답으로 transformation
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file.save('임시오디오.wav')
    return jsonify({'message': 'File uploaded successfully'})
