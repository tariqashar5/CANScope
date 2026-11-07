@echo off
if exist "dist\CANscope\CANscope.exe" (
    start "" "dist\CANscope\CANscope.exe"
) else (
    echo CANscope.exe not found! Please run install_and_build.bat first.
    pause
)