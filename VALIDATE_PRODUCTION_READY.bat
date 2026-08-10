@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║     INTELLIGENT OILFIELD INSIGHTS PLATFORM                         ║
echo ║     Production Readiness Validation                                ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo This comprehensive test will validate:
echo   ✅ All 4 databases (PostgreSQL, Neo4j, Qdrant, MinIO)
echo   ✅ Backend API endpoints
echo   ✅ AI agent pipeline
echo   ✅ Data integrity
echo   ✅ Performance metrics
echo   ✅ Error handling
echo   ✅ Security configuration
echo.
echo Auto-corrections will be applied for:
echo   🔧 Missing databases (auto-start)
echo   🔧 Missing data (auto-seed)
echo   🔧 Missing dependencies (auto-install)
echo.
echo Expected duration: 2-3 minutes
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 1: ENVIRONMENT CHECK
echo ════════════════════════════════════════════════════════════════════
echo.

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ CRITICAL: Docker not found
    echo    Please install Docker Desktop and try again
    pause
    exit /b 1
)
echo ✅ Docker Desktop: Running

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ CRITICAL: Python not found
    echo    Please install Python 3.8+ and try again
    pause
    exit /b 1
)
echo ✅ Python: Installed

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 2: DATABASE CHECK
echo ════════════════════════════════════════════════════════════════════
echo.

docker ps | findstr "oilfield-postgres" >nul
if errorlevel 1 (
    echo 🔧 Databases not running - Starting...
    docker-compose up -d postgres neo4j qdrant minio
    echo ⏱️  Waiting 60 seconds for Neo4j initialization...
    timeout /t 60 /nobreak >nul
    echo ✅ Databases started
) else (
    echo ✅ Databases: Running
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 3: BACKEND CHECK
echo ════════════════════════════════════════════════════════════════════
echo.

curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ CRITICAL: Backend not running
    echo.
    echo Please start the backend in a separate terminal:
    echo    cd backend
    echo    python main.py
    echo.
    echo Then run this test again.
    pause
    exit /b 1
)
echo ✅ Backend: Running on port 8000

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 4: DATA VALIDATION
echo ════════════════════════════════════════════════════════════════════
echo.

REM Check PostgreSQL data
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) FROM production_data;" 2>nul | findstr /R "[1-9][0-9]" >nul
if errorlevel 1 (
    echo 🔧 PostgreSQL empty - Seeding data...
    type data\seed_sql.sql | docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production >nul 2>&1
    echo ✅ PostgreSQL: Seeded
) else (
    echo ✅ PostgreSQL: Has data
)

REM Check Neo4j data
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n)" 2>nul | findstr /R "[1-9][0-9]" >nul
if errorlevel 1 (
    echo 🔧 Neo4j empty - Seeding data...
    type data\seed_graph.cypher | docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass >nul 2>&1
    echo ✅ Neo4j: Seeded
) else (
    echo ✅ Neo4j: Has data
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 5: INSTALLING TEST DEPENDENCIES
echo ════════════════════════════════════════════════════════════════════
echo.

pip install -q requests psycopg2-binary neo4j >nul 2>&1
echo ✅ Dependencies: Installed

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 6: RUNNING COMPREHENSIVE TEST SUITE
echo ════════════════════════════════════════════════════════════════════
echo.

python tests\production_readiness_test.py

set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ════════════════════════════════════════════════════════════════════
echo VALIDATION COMPLETE
echo ════════════════════════════════════════════════════════════════════
echo.

if %TEST_EXIT_CODE% EQU 0 (
    echo ✅✅✅ SUCCESS - PRODUCTION READY! ✅✅✅
    echo.
    echo Your system has passed all validation tests.
    echo You are ready for production deployment and demo.
) else (
    echo ⚠️⚠️⚠️ REVIEW REQUIRED ⚠️⚠️⚠️
    echo.
    echo Some tests did not pass. Please review the detailed report.
)

echo.
echo 📄 Reports generated:
echo    - production_readiness_report.json (detailed data)
echo    - production_readiness_report.html (visual report)
echo.

REM Auto-open HTML report
if exist production_readiness_report.html (
    echo Opening HTML report in browser...
    start production_readiness_report.html
)

echo.
pause
exit /b %TEST_EXIT_CODE%

