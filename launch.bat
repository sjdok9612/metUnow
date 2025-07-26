@echo off
setlocal enabledelayedexpansion

REM === 가상환경 폴더 이름 ===
set VENV_DIR=venv

REM === 메인 실행 파일 경로 ===
set MAIN_FILE=main.py

REM === requirements.txt 경로 ===
set REQUIREMENTS=requirements.txt

REM === Python 경로 확인 ===
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    pause
    exit /b 1
)

REM === 가상환경이 없으면 생성 ===
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo 🔧 가상환경 생성 중...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ❌ 가상환경 생성 실패
        pause
        exit /b 1
    )
)

REM === 가상환경 활성화 후 패키지 설치 ===
call "%VENV_DIR%\Scripts\activate.bat"
echo 📦 requirements.txt 설치 중...
pip install --upgrade pip >nul
pip install -r "%REQUIREMENTS%"
if errorlevel 1 (
    echo ❌ requirements.txt 설치 실패
    pause
    exit /b 1
)

REM === 명령행 인수 처리 ===
set input_file=%1
set output_dir=%2

echo target file: %input_file%
echo outpust directory: %output_dir%

REM === main.py 실행 시 인수로 넘기기 ===
echo ▶ main.py 실행 중...
python "%MAIN_FILE%" "%input_file%" "%output_dir%"
if errorlevel 1 (
    echo ❌ main.py 실행 중 오류 발생
    pause
    exit /b 1
)

pause
exit /b 0