@echo off
echo ========================================
echo Restarting Neo4j Container
echo ========================================
echo.

echo Step 1: Stopping Neo4j...
docker stop oilfield-neo4j
timeout /t 5 /nobreak >nul

echo.
echo Step 2: Starting Neo4j...
docker start oilfield-neo4j

echo.
echo Step 3: Waiting 60 seconds for Neo4j to fully initialize...
echo (Neo4j takes time to start up - please be patient)
timeout /t 60 /nobreak

echo.
echo Step 4: Checking Neo4j status...
docker ps --filter "name=oilfield-neo4j"

echo.
echo Step 5: Testing Neo4j connection...
echo.
echo Testing HTTP (port 7474)...
curl -s http://localhost:7474 >nul 2>&1
if errorlevel 1 (
    echo ❌ Neo4j HTTP is not responding yet
    echo.
    echo Neo4j might need more time. Check logs with:
    echo   docker logs oilfield-neo4j
) else (
    echo ✅ Neo4j HTTP is responding!
)

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Go to your BACKEND terminal
echo 2. Press Ctrl+C to stop the backend
echo 3. Run: python main.py
echo 4. Look for "Neo4j connection successful"
echo.
echo 5. Go to your BROWSER at http://localhost:3002
echo 6. Press F5 to refresh
echo 7. Neo4j should now show GREEN
echo.
echo If Neo4j is still offline, check the logs:
echo   docker logs oilfield-neo4j --tail 50
echo.
pause

