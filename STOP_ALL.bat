@echo off
echo ========================================
echo Stopping Intelligent Oilfield Platform
echo ========================================
echo.

echo [1/3] Stopping Backend and Frontend processes...
taskkill /FI "WindowTitle eq Oilfield Backend*" /F >nul 2>&1
taskkill /FI "WindowTitle eq Oilfield Frontend*" /F >nul 2>&1
echo ✅ Application processes stopped
echo.

echo [2/3] Stopping Database containers...
docker-compose stop
echo ✅ Database containers stopped
echo.

echo [3/3] Cleanup complete!
echo.
echo ========================================
echo Platform Stopped
echo ========================================
echo.
echo To start again, run: START_LOCAL.bat
echo.
pause

