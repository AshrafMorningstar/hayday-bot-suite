@echo off
title Hay Star - Fully Autonomous Master Runner
color 0A

echo =============================================================================
echo    🌾 HAY STAR - 100%% AUTONOMOUS MASTER RUNNER
echo    Created by Ashraf Morningstar
echo    GitHub: https://github.com/AshrafMorningstar/hay-star
echo =============================================================================
echo.

python auto_run.py
if %errorlevel% neq 0 (
    echo [ERROR] Auto runner encountered an error.
    pause
)
