@echo off
echo ========================================
echo Starting All Databases Fresh
echo ========================================
echo.

echo Neo4j is already starting...
echo Waiting 60 seconds for Neo4j to fully initialize...
timeout /t 60 /nobreak

echo.
echo Checking Neo4j status...
docker-compose ps neo4j

echo.
echo Starting other databases (PostgreSQL, Qdrant, MinIO)...
docker-compose up -d postgres qdrant minio

echo.
echo Waiting 20 seconds for other databases to start...
timeout /t 20 /nobreak

echo.
echo ========================================
echo Final Status Check:
echo ========================================
docker-compose ps

echo.
echo ========================================
echo Testing Neo4j Connection:
echo ========================================
echo.

echo Testing HTTP (7474)...
curl -s http://localhost:7474 >nul 2>&1
if errorlevel 1 (
    echo ❌ Neo4j HTTP is not responding
    echo.
    echo Check logs: docker logs oilfield-neo4j --tail 30
) else (
    echo ✅ Neo4j HTTP is responding!
)

echo.
echo Testing Bolt (7687) with cypher-shell...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test" 2>nul
if errorlevel 1 (
    echo ❌ Neo4j Bolt is not ready yet
    echo Wait another 30 seconds and try: docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1"
) else (
    echo ✅ Neo4j Bolt is working!
)

echo.
echo ========================================
echo Database URLs:
echo ========================================
echo.
echo PostgreSQL: localhost:5433
echo Neo4j Browser: http://localhost:7474
echo Neo4j Bolt: bolt://localhost:7687
echo Qdrant: http://localhost:6333
echo MinIO Console: http://localhost:9003
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. RESTART BACKEND:
echo    - Go to backend terminal
echo    - Press Ctrl+C
echo    - Run: python main.py
echo.
echo 2. REFRESH FRONTEND:
echo    - Go to http://localhost:3002
echo    - Press F5
echo    - All databases should show GREEN!
echo.
pause

