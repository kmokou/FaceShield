@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python не установлен
    echo Пожалуйста, установите Python 3.8+ по ссылке https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Перед установкой укажите, согласны ли вы с политикой конфиденциальности: https://github.com/kmokou/FaceShield/blob/main/privacy.md
echo.

set /p consent="Вы согласны с политикой конфиленциальности (Y/N): "
if /i "!consent!" neq "Y" (
    echo Установка отменена
    pause
    exit /b 1
)

echo Установка необходимых компонентов
pip install --upgrade pip
pip install -r requirements.txt

echo @echo off > run_face_shield.bat
echo setlocal >> run_face_shield.bat
echo set "SCRIPT_DIR=%%~dp0" >> run_face_shield.bat
echo cd /d "%%SCRIPT_DIR%%" >> run_face_shield.bat
echo start "" pythonw gui.py >> run_face_shield.bat

echo Установка завершена
echo Теперь вы можете запустить 'run_face_shield.bat'
pause
