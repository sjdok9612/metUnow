import subprocess
import os

def extract_audio(video_name: str):
    input_path = f"{video_name}.mp4"
    output_path = f"{video_name}.mp3"

    if not os.path.isfile(input_path):
        print(f"❌ 파일이 존재하지 않습니다: {input_path}")
        return

    command = [
        "ffmpeg",
        "-i", input_path,
        "-q:a", "0",
        "-map", "a",
        output_path
    ]

    print(f"🎬 오디오 추출 중... → {output_path}")
    subprocess.run(command, check=True)
    print("✅ 완료!")

def main():
    video_name = input("Enter the video file name(without extension): ").strip()
    extract_audio(video_name)

if __name__ == "__main__":
    main()
