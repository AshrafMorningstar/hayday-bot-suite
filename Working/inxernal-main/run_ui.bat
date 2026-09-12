@echo off
cd /d "%~dp0"
title inxernal UI Controller
echo ===================================================
echo   INXERNAL / HDX 2.5.194 BOT INTERFACE
echo ===================================================
echo Starting backend UI bridge server...
start /b python -u ui_server.py

timeout /t 2 >nul

echo Opening INXERNAL UI Window...
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:31360 --window-size=1180,780
) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:31360 --window-size=1180,780
) else (
    start http://127.0.0.1:31360
)

echo UI Active at http://127.0.0.1:31360
pause
