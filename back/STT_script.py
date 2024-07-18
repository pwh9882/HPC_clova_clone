'''
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