@echo off
setlocal enabledelayedexpansion
title CANscope Setup and Builder

echo =======================================================
echo   CANscope: Auto-Detect Environment Setup and Build
echo =======================================================
echo.

:: 1. Check existing system Python version
set "HOST_PY="
where python >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%I in ('where python') do (
        if not defined HOST_PY set "HOST_PY=%%I"
    )
)

set "NEED_STANDALONE=0"
if not defined HOST_PY (
    set "NEED_STANDALONE=1"
) else (
    for /f "tokens=2 delims= " %%v in ('"%HOST_PY%" --version 2^>^&1') do set "PY_VER=%%v"
    for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
        set "MAJOR=%%a"
        set "MINOR=%%b"
    )
    echo [*] Detected System Python: !PY_VER!
    if !MAJOR! LSS 3 set "NEED_STANDALONE=1"
    if !MAJOR! EQU 3 if !MINOR! LSS 9 set "NEED_STANDALONE=1"
)

:: 2. If Python is 3.8 or missing, attempt to fetch portable Python 3.11
set "TARGET_PY=%HOST_PY%"
if "!NEED_STANDALONE!"=="1" (
    if not exist ".python\python.exe" (
        echo [*] Older Python detected. Attempting to acquire local standalone Python 3.11...
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip', 'python_embed.zip')" >nul 2>&1
        if exist "python_embed.zip" (
            powershell -Command "Expand-Archive -Path 'python_embed.zip' -DestinationPath '.python' -Force" >nul 2>&1
            del /f /q python_embed.zip >nul 2>&1
            :: Enable site-packages in embeddable build
            powershell -Command "(Get-Content .python\*._pth) | Where-Object { $_ -ne '#import site' } | Set-Content .python\python311._pth" >nul 2>&1
            echo import site>> .python\python311._pth
            powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://bootstrap.pypa.io/get-pip.py', '.python\get-pip.py')" >nul 2>&1
            .python\python.exe .python\get-pip.py --quiet --no-warn-script-location >nul 2>&1
            del /f /q .python\get-pip.py >nul 2>&1
        )
    )
    if exist ".python\python.exe" (
        echo [*] Standalone Python 3.11 successfully initialized.
        set "TARGET_PY=%CD%\.python\python.exe"
    ) else (
        echo [!] Standalone download unavailable (firewall/offline). Falling back to host Python 3.8.
        set "TARGET_PY=%HOST_PY%"
    )
)

echo [*] Target compiler: "%TARGET_PY%"
"%TARGET_PY%" --version
echo.

:: 3. Setup dependencies
echo [*] Installing required libraries...
"%TARGET_PY%" -m pip install --upgrade pip >nul 2>&1
"%TARGET_PY%" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo.
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)

:: 4. Build executable locally
echo.
echo [*] Building local CANscope.exe...
"%TARGET_PY%" -m PyInstaller --clean -y CANscope.spec
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller compilation failed.
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