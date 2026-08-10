@echo off
echo Testing Database Status Endpoint...
echo.
curl -s http://localhost:8000/api/status/databases
echo.
echo.
pause

