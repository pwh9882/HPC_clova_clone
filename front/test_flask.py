import os

from flask import Flask, request, jsonify, render_template


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.endswith('.wav'):
        filename = file.filename
        filepath = os.path.join("C:\\Users\\ghdtj\\OneDrive\\바탕 화면\\clova\\HTC_clova_clone\\front\\uploads", filename)
        file.save(filepath)
        return jsonify({
            "message": f"File {filename} uploaded successfully"
        }), 200
    else:
        return jsonify({"error": "File type is not supported. Only .wav files are allowed"}), 400
    

if __name__ == '__main__':
    app.run(debug=True)