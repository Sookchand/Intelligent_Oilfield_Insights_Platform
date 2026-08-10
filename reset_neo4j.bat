@echo off
echo ========================================
echo Resetting Neo4j Container
echo ========================================
echo.
echo WARNING: This will delete all Neo4j data and recreate the container
echo Press Ctrl+C to cancel, or
pause
echo.

echo [1/7] Stopping and removing Neo4j container...
docker stop oilfield-neo4j 2>nul
docker rm -f oilfield-neo4j 2>nul
echo ✅ Container removed
echo.

echo [2/7] Removing Neo4j volumes...
docker volume rm intelligentOilfieldInsightPlatform_neo4j_data 2>nul
docker volume rm intelligentOilfieldInsightPlatform_neo4j_logs 2>nul
docker volume rm intelligentoilfieldinsightplatform_neo4j_data 2>nul
docker volume rm intelligentoilfieldinsightplatform_neo4j_logs 2>nul
echo ✅ Volumes removed
echo.

echo [3/7] Recreating Neo4j container...
docker-compose up -d neo4j
if %errorlevel% neq 0 (
    echo ❌ Failed to create Neo4j container
    pause
    exit /b 1
)
echo ✅ Container created
echo.

echo [4/7] Waiting 40 seconds for Neo4j to initialize...
echo This is important - Neo4j needs time to start up properly
timeout /t 40 /nobreak
echo.

echo [5/7] Checking if Neo4j is running...
docker ps | findstr neo4j
if %errorlevel% neq 0 (
    echo ❌ Neo4j container is not running!
    echo Checking logs...
    docker logs oilfield-neo4j --tail 30
    pause
    exit /b 1
)
echo ✅ Neo4j is running
echo.

echo [6/7] Testing Neo4j connection...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test"
if %errorlevel% neq 0 (
    echo ❌ Cannot connect to Neo4j
    echo Waiting another 20 seconds...
    timeout /t 20 /nobreak
    docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test"
    if %errorlevel% neq 0 (
        echo ❌ Still cannot connect. Checking logs...
        docker logs oilfield-neo4j --tail 30
        pause
        exit /b 1
    )
)
echo ✅ Neo4j connection successful
echo.

echo [7/7] Seeding Neo4j with data...
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
if %errorlevel% neq 0 (
    echo ⚠️  Seeding may have failed, but continuing...
)
echo ✅ Seeding complete
echo.

echo ========================================
echo Neo4j Reset Complete!
echo ========================================
echo.
echo Neo4j is now running and seeded with data.
echo.
echo Next steps:
echo 1. Restart the backend:
echo    cd backend
echo    ..\venv\Scripts\activate
echo    uvicorn main:app --reload
echo.
echo 2. Test in Swagger UI: http://localhost:8000/docs
echo    Execute /api/status/databases
echo.
echo 3. Refresh frontend: http://localhost:3002
echo.
pause

