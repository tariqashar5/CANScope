@echo off
title CANScope Launcher

if exist "dist\CANscope\CANscope.exe" (
    start "" "dist\CANscope\CANscope.exe"
) else (
    echo [ERROR] CANscope.exe was not found in dist\CANscope\
    echo Please run 1_run_this_once_to_install.bat first to build it.
    echo.
    pause
)