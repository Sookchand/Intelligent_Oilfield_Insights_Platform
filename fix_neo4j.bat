@echo off
echo ========================================
echo Fixing Neo4j Container
echo ========================================
echo.

echo [1/5] Starting Neo4j container...
docker start oilfield-neo4j
if %errorlevel% neq 0 (
    echo ❌ Failed to start Neo4j
    echo Trying to recreate it...
    docker-compose up -d neo4j
)
echo.

echo [2/5] Waiting 30 seconds for Neo4j to initialize...
timeout /t 30 /nobreak
echo.

echo [3/5] Checking Neo4j status...
docker ps | findstr neo4j
echo.

echo [4/5] Testing Neo4j connection...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test"
if %errorlevel% equ 0 (
    echo ✅ Neo4j is now working!
) else (
    echo ❌ Neo4j still not responding
    echo Checking logs...
    docker logs --tail 20 oilfield-neo4j
)
echo.

echo [5/5] Seeding Neo4j with data...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n) as nodes"
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
echo.

echo ========================================
echo Neo4j Fix Complete!
echo ========================================
echo.
echo Next: Restart the backend
echo   cd backend
echo   ..\venv\Scripts\activate
echo   uvicorn main:app --reload
echo.
pause

