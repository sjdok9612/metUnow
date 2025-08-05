@echo off
echo [1] Creating virtual environment...
python -m venv venv

echo [2] Activating virtual environment...
call venv\Scripts\activate

echo [3] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo [✔] Done!
pause