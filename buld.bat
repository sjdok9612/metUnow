@echo off
setlocal

REM ======= 원래 작업 디렉토리 저장 =======
set ORIGINAL_DIR=%CD%

REM ======= 설정 =======
set MAIN_FILE=main.py
set APP_NAME=MyApp
set OUTPUT_DIR=output
set DIST_DIR=%OUTPUT_DIR%\dist
set BUILD_DIR=%OUTPUT_DIR%\build
set SPEC_DIR=%OUTPUT_DIR%

REM ======= DEBUG 설정 받기 =======
set /p DEBUG=DEBUG ON PROFILE? (y/n): 

if /I "%DEBUG%"=="Y" (
    set CONSOLE_FLAG=--console
) else (
    set CONSOLE_FLAG=--noconsole
)

REM ======= spec 파일 삭제 =======
if exist "%OUTPUT_DIR%\%APP_NAME%.spec" del "%OUTPUT_DIR%\%APP_NAME%.spec"

REM ======= 빌드 시작 =======
pyinstaller %MAIN_FILE% ^
    --name %APP_NAME% ^
    --distpath %DIST_DIR% ^
    --workpath %BUILD_DIR% ^
    --specpath %SPEC_DIR% ^
    --noconfirm ^
    %CONSOLE_FLAG%

echo 빌드 완료!

REM ======= 여기부터는 추가된 복사 부분 =======
echo.
echo Copying config.json and streamers.json to final exe folder...

REM 최종 exe 폴더 경로
set EXE_FOLDER=%DIST_DIR%\%APP_NAME%

if not exist "%EXE_FOLDER%" (
    echo ERROR: Final exe folder "%EXE_FOLDER%" not found.
    goto end
)

REM config.json 복사
if exist "%ORIGINAL_DIR%\config.json" (
    copy /Y "%ORIGINAL_DIR%\config.json" "%EXE_FOLDER%\config.json"
    echo config.json copied.
) else (
    echo WARNING: config.json not found in "%ORIGINAL_DIR%"
)

REM streamers.json 복사
if exist "%ORIGINAL_DIR%\streamers.json" (
    copy /Y "%ORIGINAL_DIR%\streamers.json" "%EXE_FOLDER%\streamers.json"
    echo streamers.json copied.
) else (
    echo WARNING: streamers.json not found in "%ORIGINAL_DIR%"
)

:end
pause


