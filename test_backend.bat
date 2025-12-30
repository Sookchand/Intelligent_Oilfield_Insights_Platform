@echo off
echo Testing Backend API...
echo.

REM Wait a moment for server to be ready
timeout /t 2 /nobreak >nul

echo Testing health endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo Testing query endpoint...
curl -X POST http://localhost:8000/api/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Why is production dropping at Rig Alpha?\"}"
echo.
echo.

echo Opening API documentation in browser...
start http://localhost:8000/docs

echo.
echo Test complete!
pause

