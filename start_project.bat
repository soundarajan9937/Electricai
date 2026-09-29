@echo off
title AI Electricity Bill Analyzer

echo.
echo ==============================================
echo       AI ELECTRICITY BILL ANALYZER
echo ==============================================
echo.

REM ==============================================
REM Start Backend
REM ==============================================

echo [1/3] Starting Flask Backend...
echo.

start "Electric AI Backend" cmd /k "cd /d "%~dp0backend" && python app.py"

echo Backend is starting...
timeout /t 5 /nobreak >nul

REM ==============================================
REM Start Frontend
REM ==============================================

echo.
echo [2/3] Starting Frontend...
echo.

start "Electric AI Frontend" cmd /k "cd /d "%~dp0frontend" && python -m http.server 5500 --bind 127.0.0.1"

echo Frontend is starting...
timeout /t 3 /nobreak >nul

REM ==============================================
REM Open Chrome
REM ==============================================

echo.
echo [3/3] Opening Website in Google Chrome...
echo.

start chrome "http://127.0.0.1:5500/index.html"

echo.
echo ==============================================
echo       PROJECT STARTED SUCCESSFULLY
echo ==============================================
echo.
echo Frontend:
echo http://127.0.0.1:5500/index.html
echo.
echo Backend:
echo http://127.0.0.1:5000
echo.
echo ==============================================
echo.
echo Keep the Backend and Frontend windows open.
echo Close them when you want to stop the project.
echo.

pause
