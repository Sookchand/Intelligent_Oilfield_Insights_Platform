@echo off
echo ========================================
echo RESTARTING BACKEND WITH UPDATED CODE
echo ========================================
echo.

echo Step 1: Stopping any running Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Starting backend with updated code...
cd backend
call ..\venv\Scripts\activate.bat
echo.
echo Backend starting on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python main.py

pause

