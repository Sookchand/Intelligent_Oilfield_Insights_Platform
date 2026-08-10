@echo off
REM Quick diagnostic to check backend status

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║     BACKEND DIAGNOSTIC CHECK                                       ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

echo ════════════════════════════════════════════════════════════════════
echo STEP 1: CHECK .ENV FILE
echo ════════════════════════════════════════════════════════════════════
echo.

type .env | findstr OPENAI
echo.

echo ════════════════════════════════════════════════════════════════════
echo STEP 2: TEST BACKEND WITH SIMPLE QUERY
echo ════════════════════════════════════════════════════════════════════
echo.

echo Testing with timeout of 10 seconds...
echo.

curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d "{\"query\":\"test\"}" --max-time 10

echo.
echo.

echo ════════════════════════════════════════════════════════════════════
echo STEP 3: CHECK BACKEND PROCESS
echo ════════════════════════════════════════════════════════════════════
echo.

netstat -ano | findstr :8000

echo.
echo ════════════════════════════════════════════════════════════════════
echo ANALYSIS
echo ════════════════════════════════════════════════════════════════════
echo.
echo If the curl command timed out (took 10+ seconds):
echo   - Backend is hanging on query processing
echo   - Likely cause: Infinite loop or blocking operation
echo.
echo If the curl command returned quickly (^< 5 seconds):
echo   - Backend is working correctly
echo   - Issue is with specific test queries
echo.
echo Check your backend terminal for error messages!
echo.
pause

