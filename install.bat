@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Show privacy policy
echo Перед установкой, укажите, согласны ли вы с политикой конфиденциальности: https://github.com/kmokou/FaceShield/blob/main/privacy.md
echo.

:: Get user consent
set /p consent="Do you accept the privacy policy? (Y/N): "
if /i "!consent!" neq "Y" (
    echo Установка отменена
    pause
    exit /b 1
)

:: Install requirements
echo Установка необходимых компонентов
pip install --upgrade pip
pip install -r requirements.txt

:: Create launcher
echo Creating launcher...
echo @echo off > run_face_shield.bat
echo setlocal >> run_face_shield.bat
echo set "SCRIPT_DIR=%%~dp0" >> run_face_shield.bat
echo cd /d "%%SCRIPT_DIR%%" >> run_face_shield.bat
echo start "" pythonw gui.py >> run_face_shield.bat

echo Установка завершена
echo Теперь вы можете запустить 'run_face_shield.bat'
pause