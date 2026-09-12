@echo off
:: Hay-Star — Zero-Click Emulator Launcher
:: Double-click this file to auto-clone + launch the HayStarBot instance
:: and open Hay Day without touching anything.

title Hay-Star Emulator Launcher
color 0A
echo.
echo  ============================================================
echo    Hay-Star  Zero-Click Emulator Launcher
echo  ============================================================
echo.

:: Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install Python 3.10+ and retry.
    pause
    exit /b 1
)

:: Run the auto-setup
python "%~dp0emulator_manager.py" auto

if errorlevel 1 (
    echo.
    echo  [WARN] Emulator setup encountered issues - see above.
    pause
    exit /b 1
)

echo.
echo  Setup complete! Hay Day should now be running in HayStarBot.
echo.
timeout /t 5 >nul
