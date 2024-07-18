from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from LLM.llm_summerizer import summarize_by_llm
from STT_script import STT


app = Flask(__name__)
CORS(app)  # CORS 설정


@app.route('/')
def home():
    return render_template('index.html')


def test_init():
    # 업로드된 파일을 저장할 디렉토리 설정
    UPLOAD_FOLDER = 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def init():
    test_init()




@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.endswith('.wav'):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], "temp.wav")
        file.save(filepath)

        text = STT(filepath)
        print("text: ", text)
        summary = summarize_by_llm(text)['summary']
        print("summary: ", summary)

        return jsonify({
            "message": f"File {filename} uploaded successfully",
            "text": f"{text}",
            "summary": f"{summary}"
        }), 200
    else:
        return jsonify({"error": "File type is not supported. Only .wav files are allowed"}), 400


if __name__ == '__main__':
    init()
    # print(summarize_by_llm("대충 회의 내용 알아서 생각해서 만든 후에 요약"))
    app.run(host='0.0.0.0', port=5001, debug=True)
