#download.py
import os
import subprocess
import logging
import sys

CURRENT_FILE = os.path.abspath(__file__)    # tool/download.py의 전체 경로
TOOLS_DIR = os.path.dirname(CURRENT_FILE)   # tool/
BASE_DIR = os.path.dirname(TOOLS_DIR)       # tool/의 상위 → main.py가 있는 폴더
VOD_DIR = os.path.join(BASE_DIR, "vod")     # ./vod 경로 생성
output_dir = VOD_DIR
os.makedirs(output_dir, exist_ok=True)

def show_formats(video_url: str)-> str | None:
    """print(f"\n[1] {video_url} able list: {show_formats(video_url)}")"""
    try:
        subprocess.run(["yt-dlp", "-F", video_url], check=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ yt-dlp format not respond: {sys.executable}")
        sys.exit(1)
def get_video_title(video_url: str) -> str:
    """print(f"\n[1] {video_url} title: {get_video_title(video_url)}")"""
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", video_url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ 제목 추출 실패: {e}")
        return "unknown_title"
    
def download_video(video_url: str) -> str:
    """
    현재 함수는 선택받은 비디오ID에 대해 자동으로 다운로드를 진행합니다.
    mp4로 포맷팅 하게 되어있기 때문에, 적합한 오디오를 찾아 알아서 병합합니다.
    하지만 Video ID+Audio ID 형식으로 명시할수 있습니다.
    예시: format_id = "299+140" (비디오 ID 299, 오디오 ID 140)
    """
    print(f"\n[1] {video_url} title: {get_video_title(video_url)}")
    print(f"\n[1] {video_url} able list: {show_formats(video_url)}")
    while True:
        format_id = input("\n다운로드할 포맷 ID를 입력하세요 (예: 299+140): ").strip()
        if video_url:
            break
        print("❌ put format id")
    video_title = get_video_title(video_url)
    filename = f"{video_title}.%(ext)s"
    cmd = [
        "yt-dlp",
        "-f", format_id,
        #"--merge-output-format", "mp4",#재인코딩 필요시 화질저하. 유의
        "--external-downloader", "aria2c",
        "--external-downloader-args", "aria2c:-x 16 -s 16 -k 1M",
        "-o", os.path.join(output_dir, filename),
        video_url
    ]
    print(f"\n[2] 선택한 포맷 '{format_id}' 로 다운로드 시작...")
    try:
        subprocess.run(cmd, check=True, encoding='utf-8')
        print("✅ 다운로드 완료.")
        downloaded_ext = "mp4"  # mp4, webm 등 예상 가능
        return os.path.join(output_dir, f"{video_title}.{downloaded_ext}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 다운로드 실패: {e}")
        return ""

def main():
    while True:
        video_url = input("video URL: ").strip()
        if video_url:
            break
        print("❌ URL이 입력되지 않았습니다.")
    print(f"\n{download_video(video_url)}에 다운로드.")

if __name__ == "__main__":
    main()
