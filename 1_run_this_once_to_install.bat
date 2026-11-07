@echo off
setlocal
title CANscope Setup and Builder

echo =======================================================
echo   CANscope: Auto-Detect Environment Setup and Build
echo =======================================================
echo.

:: 1. Locate system Python
set "TARGET_PY="
where python >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%I in ('where python') do (
        if not defined TARGET_PY set "TARGET_PY=%%I"
    )
)

if not defined TARGET_PY (
    if exist "C:\Tool\python-3.8.10\python.exe" set "TARGET_PY=C:\Tool\python-3.8.10\python.exe"
)

if not defined TARGET_PY (
    echo [ERROR] No Python installation found.
    pause
    exit /b 1
)

echo [*] Found host Python: "%TARGET_PY%"
"%TARGET_PY%" --version

:: 2. Check if Python is older than 3.9 using Python directly (no batch parsing)
"%TARGET_PY%" -c "import sys; sys.exit(0 if sys.version_info < (3, 9) else 1)"
if not errorlevel 1 (
    echo [*] Python is older than 3.9. Checking for standalone Python 3.11...
    if not exist ".python\python.exe" (
        echo [*] Downloading standalone Python 3.11...
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip', 'python_embed.zip'); Expand-Archive -Path 'python_embed.zip' -DestinationPath '.python' -Force; Remove-Item 'python_embed.zip' -Force; (Get-Content .python\*._pth) | Where-Object { $_ -ne '#import site' } | Set-Content .python\python311._pth; Add-Content -Path .python\python311._pth -Value 'import site'; (New-Object System.Net.WebClient).DownloadFile('https://bootstrap.pypa.io/get-pip.py', '.python\get-pip.py'); & .python\python.exe .python\get-pip.py --quiet --no-warn-script-location; Remove-Item .python\get-pip.py -Force; exit 0 } catch { exit 1 }"
    )
    if exist ".python\python.exe" (
        echo [*] Standalone Python 3.11 ready.
        set "TARGET_PY=%CD%\.python\python.exe"
    ) else (
        echo [!] Standalone download blocked or unavailable. Falling back to host Python.
    )
)

echo.
echo [*] Using compiler: "%TARGET_PY%"
"%TARGET_PY%" --version
echo.

:: 3. Install packages
echo [*] Installing dependencies...
"%TARGET_PY%" -m pip install --upgrade pip >nul 2>&1
"%TARGET_PY%" -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo.
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)

:: 4. Build executable
echo.
echo [*] Compiling CANscope.exe...
"%TARGET_PY%" -m PyInstaller --clean -y CANscope.spec
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller build failed. Check the error output above.
    pause
    exit /b 1
)

echo.
echo =======================================================
echo   SUCCESS! CANscope has been built.
echo   Launch it using: 2_CANScope_Application.bat
echo =======================================================
echo.
pause