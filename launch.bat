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
    echo ❌ Python not installed
    pause
    exit /b 1
)

REM === 가상환경이 없으면 생성 ===
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo 🔧 make venv
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ❌ failed make venv
        pause
        exit /b 1
    )
)

REM === 가상환경 활성화 후 패키지 설치 ===
call "%VENV_DIR%\Scripts\activate.bat"
echo 📦 requirements.txt 
pip install --upgrade pip >nul
pip install -r "%REQUIREMENTS%"
if errorlevel 1 (
    echo ❌ requirements.txt failed
    pause
    exit /b 1
)

REM === main.py 실행 시 인수로 넘기기 ===
echo ▶ main.py 
python "%MAIN_FILE%"
if errorlevel 1 (
    echo ❌ main.py error
    pause
    exit /b 1
)

pause
exit /b 0