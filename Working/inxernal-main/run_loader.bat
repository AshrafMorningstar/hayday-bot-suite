@echo off
cd /d "%~dp0"
title inxernal console
echo Starting inxernal loader...
python -u loader.py %*
pause
