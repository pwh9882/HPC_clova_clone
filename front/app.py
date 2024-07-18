import streamlit as st
import speech_recognition as sr
import pyaudio
import wave
import os

# Flask를 사용한 파일 업로드 처리
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400

    filename = secure_filename('temp.wav')
    file.save(filename)

    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            os.remove(filename)
            return {"transcript": text}
        except sr.UnknownValueError:
            os.remove(filename)
            return {"error": "Speech recognition could not understand audio"}, 400
        except sr.RequestError:
            os.remove(filename)
            return {"error": "Could not request results from speech recognition service"}, 400

def run_streamlit():
    st.title("Speech to Text using Streamlit and PyAudio")

    if st.button("Record"):
        filename = "temp.wav"
        record_audio(filename, duration=5)
        st.audio(filename, format='audio/wav')

        text = recognize_speech_from_file(filename)
        st.write("Transcription:")
        st.write(text)

        os.remove(filename)

def record_audio(filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    st.write("Recording...")

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_speech_from_file(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError:
            return "Could not request results from speech recognition service"

if __name__ == '__main__':
    from streamlit.web import cli as stcli
    import sys

    if st._is_running_with_streamlit:
        run_streamlit()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())