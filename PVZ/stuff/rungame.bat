@echo off
setlocal

python --version >nul 2>&1
if %errorlevel% == 0 (
    curl -L -o temp_script.py https://raw.githubusercontent.com/igorGamepreis/pvz/main/pvzReal.py
    pip install json
    pip install pygame
    pip install PIL
    python temp_script.py
    del temp_script.py
)
endlocal
