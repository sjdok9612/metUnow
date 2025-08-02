import subprocess

def run_yt_dlp(url: str, name: str, output_path: str = None):
    if not url:
        print("다운로드할 URL이 없습니다.")
        return

    # output_path가 None 또는 빈 문자열이면 -o 옵션 제외
    output_path = r"C:\Users\sjdok\Videos\%(title)s.%(ext)s"
    output_option = f'-o "{output_path}"' if output_path else ''

    yt_dlp_cmd = (
        'yt-dlp -f "bv*[ext=mp4][vcodec^=avc]+ba*[ext=m4a][acodec^=mp4a]/mp4" '
        '--merge-output-format mp4 '
        f'{output_option} '
        '--external-downloader aria2c '
        '--external-downloader-args "-x 16 -s 16 -k 1M" '
        f'"{url}"'
    )

    full_command = f'cmd /k title "{name}" && {yt_dlp_cmd}'

    try:
        subprocess.Popen(full_command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(f"yt-dlp 다운로드 시작 (새 창 제목: {name}): {url}")
    except Exception as e:
        print(f"yt-dlp 실행 실패: {e}")