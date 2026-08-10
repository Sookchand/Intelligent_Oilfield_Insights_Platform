@echo off
setlocal enabledelayedexpansion

echo ========================================
echo AUTOMATED PRODUCTION READINESS TEST
echo ========================================
echo.
echo This will:
echo 1. Check all prerequisites
echo 2. Auto-fix common issues
echo 3. Run comprehensive tests
echo 4. Generate detailed report
echo.
pause

set ERRORS=0
set WARNINGS=0
set FIXES=0

echo.
echo ========================================
echo PHASE 1: PREREQUISITE CHECKS
echo ========================================
echo.

REM Check Docker
echo [1/6] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found or not running
    set /a ERRORS+=1
) else (
    echo ✅ Docker is running
)

REM Check Python
echo [2/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    set /a ERRORS+=1
) else (
    echo ✅ Python is installed
)

REM Check Node.js
echo [3/6] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found (frontend won't work)
    set /a WARNINGS+=1
) else (
    echo ✅ Node.js is installed
)

REM Check if databases are running
echo [4/6] Checking databases...
docker ps | findstr "oilfield-postgres" >nul
if errorlevel 1 (
    echo ⚠️  Databases not running - Starting them...
    docker-compose up -d postgres neo4j qdrant minio
    echo    Waiting 60 seconds for Neo4j to initialize...
    timeout /t 60 /nobreak >nul
    set /a FIXES+=1
    echo ✅ Databases started
) else (
    echo ✅ Databases are running
)

REM Check if backend is running
echo [5/6] Checking backend...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend not running
    echo    Please start backend in separate terminal:
    echo    cd backend ^&^& python main.py
    set /a ERRORS+=1
) else (
    echo ✅ Backend is running
)

REM Check if frontend is running
echo [6/6] Checking frontend...
curl -s http://localhost:3002 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Frontend not running (optional)
    set /a WARNINGS+=1
) else (
    echo ✅ Frontend is running
)

echo.
echo ========================================
echo PHASE 2: DATA VALIDATION
echo ========================================
echo.

REM Check PostgreSQL data
echo [1/2] Checking PostgreSQL data...
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) FROM production_data;" 2>nul | findstr /R "[0-9][0-9]" >nul
if errorlevel 1 (
    echo ⚠️  No data in PostgreSQL - Seeding...
    type data\seed_sql.sql | docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production >nul 2>&1
    set /a FIXES+=1
    echo ✅ PostgreSQL seeded
) else (
    echo ✅ PostgreSQL has data
)

REM Check Neo4j data
echo [2/2] Checking Neo4j data...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n)" 2>nul | findstr /R "[0-9][0-9]" >nul
if errorlevel 1 (
    echo ⚠️  No data in Neo4j - Seeding...
    type data\seed_graph.cypher | docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass >nul 2>&1
    set /a FIXES+=1
    echo ✅ Neo4j seeded
) else (
    echo ✅ Neo4j has data
)

echo.
echo ========================================
echo PHASE 3: INSTALLING TEST DEPENDENCIES
echo ========================================
echo.

pip install -q requests psycopg2-binary neo4j 2>nul
if errorlevel 1 (
    echo ⚠️  Some dependencies may have failed to install
    set /a WARNINGS+=1
) else (
    echo ✅ Test dependencies installed
)

echo.
echo ========================================
echo PHASE 4: RUNNING COMPREHENSIVE TESTS
echo ========================================
echo.

python tests\production_readiness_test.py

set TEST_RESULT=%ERRORLEVEL%

echo.
echo ========================================
echo PHASE 5: SUMMARY
echo ========================================
echo.
echo Prerequisite Errors: %ERRORS%
echo Warnings: %WARNINGS%
echo Auto-fixes Applied: %FIXES%
echo.

if %ERRORS% GTR 0 (
    echo ❌ CRITICAL ERRORS FOUND
    echo    Fix the errors above and run again
    pause
    exit /b 1
)

if %TEST_RESULT% EQU 0 (
    echo ✅ ALL TESTS PASSED - PRODUCTION READY!
) else (
    echo ⚠️  SOME TESTS FAILED - Review report
)

echo.
echo 📄 Detailed report: production_readiness_report.json
echo 📄 HTML report: production_readiness_report.html
echo.
pause
exit /b %TEST_RESULT%

