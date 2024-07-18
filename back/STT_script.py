'''
<<<<<<< HEAD
audio형식의 file(wav) --> text
parameter로 audio file의 path를 받아옴
return값 : .txt이 아닌 string 형식의 text
'''

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
    )

def STT(wav_file_path):
    
    with open(wav_file_path, 'rb') as audio_file :
    
        response = client.audio.transcriptions.create(
            model = 'whisper-1',
            file=audio_file,
            response_format = 'text'
        )
    return response

if __name__ == "__main__":
    #경로
    audio_file_path = "/Users/newuser/HTC_clova_clone/back/샘플.wav"

    transcribed_text = STT(audio_file_path)
    print(transcribed_text)
=======
audio형식의 file(wav) -> text
parameter로 audio file의 path를 받아옴
return값 : .txt이 아닌 string 형식의 text
'''
import whisper

def STT(wav_file_path):

    # Whisper 모델 불러오기
    model = whisper.load_model("base")
    
    # 오디오 파일을 텍스트로 변환
    result = model.transcribe(wav_file_path)
    
    # 변환된 텍스트 반환
    return result["text"]

audio_file_path = "newuser/file.wav"

transcribed_text = STT(audio_file_path)
print(transcribed_text)
>>>>>>> 4fb7057339bc9b47d7c99773b15b0429dd6f84c2
