@echo off
title Hay Star - Test Suite
cls
cd /d "%~dp0\.."
echo ======================================================================
echo   Hay Star - Complete System Test Suite
echo   Ashraf Morningstar
echo ======================================================================
echo.
python tests/test_all.py
echo.
pause
