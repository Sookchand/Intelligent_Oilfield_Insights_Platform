@echo off
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     PRODUCTION READINESS TEST - QUICK VERSION              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Quick prerequisite check
echo Checking prerequisites...
echo.

docker ps | findstr "oilfield-postgres" >nul
if errorlevel 1 (
    echo ❌ Databases not running
    echo.
    echo Starting databases...
    docker-compose up -d postgres neo4j qdrant minio
    echo Waiting 60 seconds for initialization...
    timeout /t 60 /nobreak >nul
)

curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend not running
    echo.
    echo Please start backend:
    echo    cd backend
    echo    python main.py
    echo.
    pause
    exit /b 1
)

echo ✅ All prerequisites met
echo.
echo Running tests...
echo.

python tests\production_readiness_test.py

if errorlevel 1 (
    echo.
    echo ⚠️  Some tests failed - Check report for details
) else (
    echo.
    echo ✅ All tests passed!
)

echo.
echo 📄 View detailed report: production_readiness_report.html
echo.

REM Auto-open HTML report
if exist production_readiness_report.html (
    start production_readiness_report.html
)

pause

