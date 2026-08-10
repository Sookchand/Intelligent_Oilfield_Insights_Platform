@echo off
echo ========================================
echo Database Connection Diagnostic and Fix
echo ========================================
echo.

echo [Step 1/8] Checking Docker containers...
echo.
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo [Step 2/8] Testing Neo4j directly...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test" 2>&1
if %errorlevel% equ 0 (
    echo ✅ Neo4j direct connection: SUCCESS
) else (
    echo ❌ Neo4j direct connection: FAILED
    echo Attempting to fix Neo4j...
    docker restart oilfield-neo4j
    echo Waiting 20 seconds for Neo4j to restart...
    timeout /t 20 /nobreak >nul
)
echo.

echo [Step 3/8] Testing Qdrant directly...
curl -s http://localhost:6333/collections 2>&1 | findstr "result" >nul
if %errorlevel% equ 0 (
    echo ✅ Qdrant direct connection: SUCCESS
) else (
    echo ❌ Qdrant direct connection: FAILED
    echo Attempting to fix Qdrant...
    docker restart oilfield-qdrant
    echo Waiting 15 seconds for Qdrant to restart...
    timeout /t 15 /nobreak >nul
)
echo.

echo [Step 4/8] Testing PostgreSQL directly...
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT 1" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL direct connection: SUCCESS
) else (
    echo ❌ PostgreSQL direct connection: FAILED
)
echo.

echo [Step 5/8] Testing MinIO directly...
curl -s http://localhost:9002 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MinIO direct connection: SUCCESS
) else (
    echo ❌ MinIO direct connection: FAILED
)
echo.

echo [Step 6/8] Checking backend .env file...
if exist backend\.env (
    echo ✅ .env file exists
    echo.
    echo Key configuration values:
    findstr "NEO4J_URI" backend\.env
    findstr "NEO4J_PASSWORD" backend\.env
    findstr "QDRANT_HOST" backend\.env
    findstr "QDRANT_PORT" backend\.env
) else (
    echo ❌ .env file missing!
    echo Creating .env file...
    copy backend\.env.example backend\.env
)
echo.

echo [Step 7/8] Testing backend Python connections...
cd backend
call ..\venv\Scripts\activate
python test_connections.py
cd ..
echo.

echo [Step 8/8] Final verification...
echo.
echo Testing Neo4j again...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Neo4j: WORKING
) else (
    echo ❌ Neo4j: STILL FAILING
)

echo Testing Qdrant again...
curl -s http://localhost:6333/collections >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Qdrant: WORKING
) else (
    echo ❌ Qdrant: STILL FAILING
)
echo.

echo ========================================
echo Diagnostic Complete
echo ========================================
echo.
echo Next steps:
echo 1. If databases are working, restart backend:
echo    cd backend
echo    ..\venv\Scripts\activate
echo    uvicorn main:app --reload
echo.
echo 2. Then test in Swagger UI:
echo    http://localhost:8000/docs
echo    Test /api/status/databases endpoint
echo.
echo 3. Refresh frontend:
echo    http://localhost:3002
echo.
pause

