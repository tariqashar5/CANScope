@echo off
setlocal
title CANscope Setup and Builder

echo =======================================================
echo   CANscope: One-Click Environment Setup and Build
echo =======================================================
echo.

:: 1. Verify Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in your PATH.
    echo Please make sure Python 3.10+ is installed and added to PATH.
    echo.
    pause
    exit /b 1
)

:: 2. Setup local virtual environment
if not exist ".venv" (
    echo [*] Creating isolated virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: 3. Install dependencies
echo [*] Installing required packages...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies from requirements.txt.
    pause
    exit /b 1
)

:: 4. Verify spec file exists
if not exist "CANscope.spec" (
    echo [ERROR] CANscope.spec was not found in the current folder: %CD%
    echo Please verify the spec filename.
    pause
    exit /b 1
)

:: 5. Build executable
echo [*] Compiling CANscope.exe locally...
python -m PyInstaller --clean -y CANscope.spec
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller compilation failed! Look above for the Python error.
    pause
    exit /b 1
)

echo.
echo =======================================================
echo   SUCCESS! CANscope has been compiled.
echo   You can now launch the app using:
echo   2_CANScope_Application.bat
echo =======================================================
echo.
pause