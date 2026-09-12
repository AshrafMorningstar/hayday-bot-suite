@echo off
title Hay Star - Autonomous Farm Suite by Ashraf Morningstar
color 0B
cd /d "%~dp0"

echo =============================================================================
echo    🌾 HAY STAR - COMPLETE AUTONOMOUS FARMING & MOD SUITE 🌾
echo    Created by Ashraf Morningstar | https://github.com/AshrafMorningstar/hay-star
echo =============================================================================
echo    Shortcuts: hv=Harvest, pl=Plant, ss=Sell, cc=Coins, j=Jump, af=AutoFarm
echo               mn=Mine, fh=Fish, as=Accounts, cr=Config, em=Emulator, s=Search, h=Help, x=Stop
echo =============================================================================
echo.

:: Check Python and route CLI arguments
python --version >nul 2>&1
if %errorlevel% equ 0 (
    if "%~1"=="" (
        python launcher.py
    ) else (
        python launcher.py %*
    )
) else (
    echo [WARN] Python not found in PATH. Launching native hay-star.exe directly...
    if exist "hay-star.exe" (
        hay-star.exe %*
    ) else (
        echo [ERROR] Neither Python nor hay-star.exe was found!
        echo Please install Python 3.9+ or run install.bat.
        pause
    )
)

pause
