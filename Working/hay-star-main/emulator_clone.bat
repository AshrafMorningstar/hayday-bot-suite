@echo off
:: Hay-Star — Clone Emulator Instance Only
:: Creates HayStarBot as a copy of LDPlayer (does not launch it).

title Hay-Star Emulator Clone
color 0B
echo.
echo  ============================================================
echo    Hay-Star  Emulator Instance Cloner
echo  ============================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found.
    pause & exit /b 1
)

set /p SRC="  Source instance name [LDPlayer]: "
if "%SRC%"=="" set SRC=LDPlayer
set /p DEST="  Destination instance name [HayStarBot]: "
if "%DEST%"=="" set DEST=HayStarBot

echo.
echo  Cloning %SRC% -> %DEST%...
python "%~dp0emulator_manager.py" clone "%SRC%" "%DEST%"

if errorlevel 1 (
    echo  [ERROR] Clone failed.
    pause & exit /b 1
)

echo.
echo  Clone complete! Run launch_emulator.bat to start it.
echo.
pause
