@echo off
setlocal enabledelayedexpansion

set input_file=C:\Users\sjdok\tools\VODloader\vods\혼자는 못 나가는 방 ｜ 미라이 20화(w. 오몽, 마젯, 오요, 하지유, 희지) [OE0cXlOQHDw].mp4
set output_dir=C:\Users\sjdok\tools\VODloader\vods\

REM 
echo target file: %input_file%
echo outputs : %output_dir%

call launch.bat "%input_file%" "%output_dir%"

pause
exit /b 0