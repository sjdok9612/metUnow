import os
import subprocess

def download_video(video_url: str) -> str | None:
    output_dir = "vods"
    os.makedirs(output_dir, exist_ok=True)

    if not video_url.strip():
        print("❌ URL이 입력되지 않았습니다.")
        return None

    get_filename_cmd = [
        "yt-dlp",
        "--print", "%(title)s.%(ext)s",
        "-f", 'bv*[ext=mp4][vcodec^=avc]+ba*[ext=m4a][acodec^=mp4a]/mp4',
        video_url
    ]
    try:
        result = subprocess.run(get_filename_cmd, capture_output=True, text=True, encoding='utf-8', check=True)
        filename = result.stdout.strip()
        filename_wo_ext = os.path.splitext(filename)[0]  # 확장자 제거
        full_path = os.path.join(output_dir, filename_wo_ext)
    except subprocess.CalledProcessError as e:
        print(f"❌ 파일명 추출 실패: {e}")
        return None

    ytdlp_command = [
        "yt-dlp",
        "-f", 'bv*[ext=mp4][vcodec^=avc]+ba*[ext=m4a][acodec^=mp4a]/mp4',
        "--merge-output-format", "mp4",
        "--external-downloader", "aria2c",
        "--external-downloader-args", "-x 16 -s 16 -k 1M",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        video_url
    ]

    try:
        subprocess.run(ytdlp_command, check=True, text=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"❌ 다운로드 실패: {e}")
        return None
    else:
        print("✅ 다운로드 완료.")
        return full_path
def main():
    video_url: str = input("비디오 URL을 입력하세요: ").strip()
    download_video(video_url)
if __name__ == "__main__":
    main()