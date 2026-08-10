@echo off
echo ========================================
echo Restarting Backend with LangSmith
echo ========================================
echo.

echo [1/3] Stopping any running backend...
echo ----------------------------------------
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*" 2>nul
timeout /t 2 /nobreak > nul
echo Done.
echo.

echo [2/3] Starting backend with LangSmith...
echo ----------------------------------------
cd backend
call ..\venv\Scripts\activate
echo.
echo Starting backend... (Watch for LangSmith confirmation)
echo.
python main.py

