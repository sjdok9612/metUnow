import whisper
import numpy as np
import torchaudio

def load_audio_from_file(file_path: str, sr: int = 16000) -> tuple[np.ndarray, int]:
    """
    WAV 파일을 numpy 배열로 로드
    """
    waveform, sample_rate = torchaudio.load(file_path)
    if sample_rate != sr:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=sr)(waveform)
    return waveform.squeeze(0).numpy(), sr


def transcribe_whisper(audio: np.ndarray, sr: int = 16000, model_size: str = "base") -> dict:
    """
    Whisper로 오디오를 텍스트로 변환
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio=audio, language="ko", fp16=False)
    return result


if __name__ == "__main__":
    # 1. WAV 파일 불러오기
    wav_path = "example.wav"
    audio_np, sr = load_audio_from_file(wav_path)

    # 2. Whisper 인식
    result = transcribe_whisper(audio_np, sr, model_size="base")

    # 3. 출력
    print(result["text"])
