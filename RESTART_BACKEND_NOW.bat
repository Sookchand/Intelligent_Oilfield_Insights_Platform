@echo off
echo ================================================================================
echo Restarting Backend with New Fixes
echo ================================================================================
echo.

echo [1/2] Stopping existing backend...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo   Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)
echo   Done
timeout /t 2 /nobreak >nul

echo.
echo [2/2] Starting backend with new fixes...
echo   - PostgreSQL parameter conversion
echo   - Intelligent result formatting
echo.

cd backend
call ..\venv\Scripts\activate.bat
python main.py

