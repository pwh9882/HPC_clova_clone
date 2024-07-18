from flask import Flask, request, jsonify
import speech_recognition as sr
import wave
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    filename = 'temp.wav'
    file.save(filename)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            os.remove(filename)
            return jsonify({"transcript": text})
        except sr.UnknownValueError:
            os.remove(filename)
            return jsonify({"error": "Speech recognition could not understand audio"})
        except sr.RequestError:
            os.remove(filename)
            return jsonify({"error": "Could not request results from speech recognition service"})

if __name__ == '__main__':
    app.run(debug=True)
