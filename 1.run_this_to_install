@echo off
setlocal
title CANscope Setup & Builder

echo =======================================================
echo   CANscope: One-Click Environment Setup & Build
echo =======================================================
echo.

:: 1. Verify Python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in your PATH.
    echo Please install Python 3.10+ and make sure "Add Python to PATH" is checked.
    echo.
    pause
    exit /b 1
)

:: 2. Setup a local isolated virtual environment
if not exist ".venv" (
    echo [*] Creating isolated virtual environment (.venv)...
    python -m venv .venv
)

:: 3. Install dependencies inside the virtual environment
echo [*] Installing required packages...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt pyinstaller

:: 4. Build the local standalone executable
echo [*] Compiling CANscope.exe locally...
pyinstaller --clean -y CANscope.spec

:: 5. Create a direct Desktop shortcut (optional convenience)
echo.
echo =======================================================
echo   SUCCESS! CANscope is ready.
echo   Location: dist\CANscope\CANscope.exe
echo =======================================================
echo.
pause