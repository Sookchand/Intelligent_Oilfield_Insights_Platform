@echo off
echo ========================================
echo PRODUCTION READINESS TEST SUITE
echo ========================================
echo.

echo Prerequisites Check:
echo ========================================
echo.

echo [1/4] Checking if databases are running...
docker ps | findstr "oilfield-postgres" >nul
if errorlevel 1 (
    echo ❌ PostgreSQL not running
    echo    Run: docker-compose up -d
    pause
    exit /b 1
)
echo ✅ Databases running
echo.

echo [2/4] Checking if backend is running...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend not running
    echo    Start backend: cd backend ^&^& python main.py
    pause
    exit /b 1
)
echo ✅ Backend running
echo.

echo [3/4] Checking if frontend is running...
curl -s http://localhost:3002 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Frontend not running (optional for API tests)
    echo    Start frontend: cd frontend ^&^& npm run dev
) else (
    echo ✅ Frontend running
)
echo.

echo [4/4] Installing test dependencies...
pip install requests psycopg2-binary neo4j >nul 2>&1
echo ✅ Dependencies ready
echo.

echo ========================================
echo Running Production Readiness Tests
echo ========================================
echo.

cd %~dp0
python tests\production_readiness_test.py

echo.
echo ========================================
echo Test Complete
echo ========================================
echo.
echo Check production_readiness_report.json for detailed results
echo.
pause

