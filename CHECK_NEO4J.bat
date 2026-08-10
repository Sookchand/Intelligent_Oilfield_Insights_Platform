@echo off
echo ========================================
echo Neo4j Diagnostic Check
echo ========================================
echo.

echo Checking Neo4j container status...
docker ps -a --filter "name=oilfield-neo4j"
echo.

echo ========================================
echo Neo4j Container Logs (last 30 lines):
echo ========================================
docker logs oilfield-neo4j --tail 30
echo.

echo ========================================
echo Testing Neo4j Connection:
echo ========================================
echo.
echo Testing HTTP endpoint...
curl -s http://localhost:7474 >nul 2>&1
if errorlevel 1 (
    echo ❌ Neo4j HTTP (7474) is NOT responding
) else (
    echo ✅ Neo4j HTTP (7474) is responding
)
echo.

echo Testing Bolt endpoint...
powershell -Command "Test-NetConnection -ComputerName localhost -Port 7687 -InformationLevel Quiet"
if errorlevel 1 (
    echo ❌ Neo4j Bolt (7687) is NOT accessible
) else (
    echo ✅ Neo4j Bolt (7687) is accessible
)
echo.

echo ========================================
echo Recommended Actions:
echo ========================================
echo.
echo If Neo4j is not running:
echo   1. docker restart oilfield-neo4j
echo   2. Wait 30 seconds
echo   3. Run this script again
echo.
echo If Neo4j keeps failing:
echo   1. docker-compose down
echo   2. docker volume rm intelligentoilfieldinsightplatform_neo4j_data
echo   3. docker-compose up -d neo4j
echo.
pause

