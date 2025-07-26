import sys
import os
import subprocess
from pyannote.audio import Pipeline
from pydub import AudioSegment
import whisper
from datetime import timedelta
import torch

# ==== 설정 ====
INPUT_DIR = "vods/"
INPUT_FILENAME_BASE = "바삭토스트의 라이브 방송"
INPUT_EXT = "mp3"

INPUT_FILENAME = f"{INPUT_FILENAME_BASE}.{INPUT_EXT}"
INPUT_FILE = os.path.join(INPUT_DIR, INPUT_FILENAME)

TEMP_WAV = "audio.wav"
HUGGINGFACE_TOKEN = "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"
WHISPER_MODEL = "large"

# ==== 디바이스 설정 ====
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"⚙️ 사용 디바이스: {DEVICE}")

# ==== 1. 오디오 추출 ====
def extract_audio(input_path, output_wav):
    try:
        ext = os.path.splitext(input_path)[1].lower()
        print(f"🎬 입력 파일: {input_path}")
        if ext in [".mp4", ".mkv"]:
            print(f"🔄 {ext[1:].upper()}에서 오디오 추출 중 (16000Hz, mono)...")
            completed = subprocess.run([
                "ffmpeg", "-y", "-i", input_path,
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_wav
            ], capture_output=True, text=True)
            if completed.returncode != 0:
                print(f"❌ ffmpeg 오류:\n{completed.stderr}")
                sys.exit(1)
            print(f"✅ 오디오 추출 완료 → {output_wav}")
        else:
            print("🎧 오디오 파일 변환 중 (16000Hz, mono)...")
            audio = AudioSegment.from_file(input_path).set_frame_rate(16000).set_channels(1)
            audio.export(output_wav, format="wav")
            print(f"✅ 오디오 변환 완료 → {output_wav}")
    except Exception as e:
        print(f"❌ 오디오 추출/변환 중 예외 발생: {e}")
        sys.exit(1)

# ==== 2. 화자 분리 ====
def diarize_audio(wav_path, token):
    try:
        print("🔍 화자 분리 모델 로딩 중...")
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=token)
        pipeline.to(DEVICE)  # ✅ CUDA 사용 명시
        print("👤 화자 분리 수행 중...")
        diarization = pipeline(wav_path)
        print("✅ 화자 분리 완료")
        return diarization
    except Exception as e:
        print(f"❌ 화자 분리 중 예외 발생: {e}")
        sys.exit(1)

# ==== 3. Whisper 음성 인식 ====
def transcribe_segments(wav_path, diarization, model):
    try:
        print("🗣 Whisper 음성 인식 시작...")
        audio = AudioSegment.from_wav(wav_path)
        results = []
        segments = list(diarization.itertracks(yield_label=True))
        total = len(segments)
        for i, (turn, _, speaker) in enumerate(segments, 1):
            percent = (i / total) * 100
            print(f"▶ [{i}/{total}] ({percent:.1f}%) 화자: {speaker} | 시간: {turn.start:.1f}s ~ {turn.end:.1f}s")
            start_ms = int(turn.start * 1000)
            end_ms = int(turn.end * 1000)
            segment = audio[start_ms:end_ms]
            segment_path = f"temp_{speaker}_{start_ms}.wav"
            segment.export(segment_path, format="wav")

            print("🔈 Whisper 처리 중...")
            whisper_result = model.transcribe(
                segment_path,
                language="ko",
                fp16=torch.cuda.is_available(),  # ✅ mixed precision if using CUDA
            )
            text = whisper_result.get("text", "").strip()
            os.remove(segment_path)

            print(f"📝 인식 결과: {text[:50]}{'...' if len(text) > 50 else ''}")
            results.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker,
                "text": text
            })
        print("✅ Whisper 인식 전체 완료")
        return results
    except Exception as e:
        print(f"❌ Whisper 인식 중 예외 발생: {e}")
        sys.exit(1)

# ==== 4. 결과 출력 ====
def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

def write_output(results, output_file="transcript.txt"):
    try:
        print(f"💾 결과 파일 저장 중 → {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"[{format_time(r['start'])}] {r['speaker']}: {r['text']}\n")
        print(f"✅ 저장 완료: {output_file}")
    except Exception as e:
        print(f"❌ 결과 저장 중 예외 발생: {e}")
        sys.exit(1)

# ==== 실행 ====
def main():
    if not os.path.exists(INPUT_FILE):
        print("INPUT_FILE 경로:", INPUT_FILE)
        print("파일 존재 여부:", os.path.exists(INPUT_FILE))
        sys.exit(1)

    extract_audio(INPUT_FILE, TEMP_WAV)

    diarization = diarize_audio(TEMP_WAV, HUGGINGFACE_TOKEN)

    try:
        whisper_model = whisper.load_model(WHISPER_MODEL, device=str(DEVICE))  # ✅ CUDA 모델 로딩
        print("📦 Whisper 모델 로딩 완료")
    except Exception as e:
        print(f"❌ Whisper 모델 로딩 중 예외 발생: {e}")
        sys.exit(1)

    results = transcribe_segments(TEMP_WAV, diarization, whisper_model)

    # 임시 전체 오디오 파일 삭제
    if os.path.exists(TEMP_WAV):
        os.remove(TEMP_WAV)
        print(f"🧹 임시 파일 삭제 완료: {TEMP_WAV}")
        
    # 출력 파일 이름 자동 생성 (mp3 → txt)
    base_name = os.path.splitext(INPUT_FILENAME)[0]
    output_txt = os.path.join(INPUT_DIR, f"{base_name}.txt")

    write_output(results, output_txt)

if __name__ == "__main__":
    main()
