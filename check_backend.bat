@echo off
echo ============================================================
echo CHECKING BACKEND STATUS
echo ============================================================
echo.

echo Checking if port 8000 is in use...
netstat -ano | findstr :8000
echo.

echo Checking Python processes...
tasklist | findstr python.exe
echo.

echo Attempting to connect to backend...
curl -s http://localhost:8000/api/status/databases
echo.

echo ============================================================
echo If you see JSON output above, backend is running!
echo If you see "Failed to connect" or nothing, backend is NOT running.
echo ============================================================
pause

