@echo off
echo ========================================
echo Database Connection Fix Script
echo ========================================
echo.

echo [1/6] Checking Docker containers...
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr oilfield
echo.

echo [2/6] Restarting Qdrant (often unhealthy)...
docker restart oilfield-qdrant
echo Waiting 10 seconds for Qdrant to start...
timeout /t 10 /nobreak >nul
echo.

echo [3/6] Testing Neo4j connection...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test" 2>nul
if errorlevel 1 (
    echo    ❌ Neo4j connection failed
    echo    Trying to reset Neo4j password...
    docker restart oilfield-neo4j
    timeout /t 15 /nobreak >nul
) else (
    echo    ✅ Neo4j connected
)
echo.

echo [4/6] Testing Qdrant connection...
curl -s http://localhost:6333/collections >nul 2>&1
if errorlevel 1 (
    echo    ❌ Qdrant not responding
    echo    Restarting Qdrant again...
    docker restart oilfield-qdrant
    timeout /t 10 /nobreak >nul
) else (
    echo    ✅ Qdrant connected
)
echo.

echo [5/6] Testing PostgreSQL connection...
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo    ❌ PostgreSQL connection failed
) else (
    echo    ✅ PostgreSQL connected
)
echo.

echo [6/6] Testing MinIO connection...
curl -s http://localhost:9002 >nul 2>&1
if errorlevel 1 (
    echo    ❌ MinIO not responding
) else (
    echo    ✅ MinIO connected
)
echo.

echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure backend is running: uvicorn main:app --reload
echo 2. Refresh the frontend at http://localhost:3001
echo 3. Check database status in the UI
echo.
pause

