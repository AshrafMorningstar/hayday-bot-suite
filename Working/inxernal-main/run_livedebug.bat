@echo off
cd /d "%~dp0"
title inxernal Live Debugger
echo ===================================================
echo   INXERNAL LIVE DEBUGGING ENVIRONMENT
echo ===================================================
python -u loader.py --livedebug %*
pause
