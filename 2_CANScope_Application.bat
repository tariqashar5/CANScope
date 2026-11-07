@echo off
setlocal
title CANScope Launcher

:: Check for compiled executable
if exist "dist\CANscope\CANscope.exe" (
    start "" "dist\CANscope\CANscope.exe"
    exit /b 0
)

:: Direct script launch fallback if .exe was restricted
if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\streamlit.exe" run app.py
    exit /b 0
)

if exist ".lib" (
    set "PYTHONPATH=%CD%\.lib;%PYTHONPATH%"
    python -m streamlit run app.py
    exit /b 0
)

echo [ERROR] Application not ready.
echo Please run 1_run_this_once_to_install.bat first.
pause