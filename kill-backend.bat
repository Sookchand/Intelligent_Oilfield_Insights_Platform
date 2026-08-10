@echo off
echo Killing backend process on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Killing process ID: %%a
    taskkill /F /PID %%a
)
echo Done!
timeout /t 2 /nobreak >nul

