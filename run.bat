@echo off
title 🌾 Hay Day Bot Suite — 1-Click Farm Control Center
color 0A
cd /d "%~dp0"

python start_bot.py %*
if errorlevel 1 (
    echo.
    echo  [!] Process exited. Press any key to close.
    pause
)
