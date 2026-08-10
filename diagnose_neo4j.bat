@echo off
echo ========================================
echo NEO4J DIAGNOSTIC SCRIPT
echo ========================================
echo.

echo [1/8] Checking Docker containers...
echo ----------------------------------------
docker-compose ps
echo.

echo [2/8] Checking if Neo4j container exists...
echo ----------------------------------------
docker ps -a | findstr neo4j
echo.

echo [3/8] Checking Neo4j logs (last 30 lines)...
echo ----------------------------------------
docker logs oilfield-neo4j --tail 30
echo.

echo [4/8] Testing Neo4j connection from host...
echo ----------------------------------------
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test"
echo.

echo [5/8] Checking Neo4j data (node count)...
echo ----------------------------------------
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n) as total_nodes"
echo.

echo [6/8] Checking Python packages...
echo ----------------------------------------
call venv\Scripts\activate
pip list | findstr neo4j
pip list | findstr qdrant
echo.

echo [7/8] Testing Python connection to Neo4j...
echo ----------------------------------------
cd backend
python -c "from database.connections import get_neo4j_driver; driver = get_neo4j_driver(); print('✅ Neo4j driver created'); driver.close()"
cd ..
echo.

echo [8/8] Full connection test...
echo ----------------------------------------
cd backend
python -c "from database.connections import test_all_connections; import json; print(json.dumps(test_all_connections(), indent=2))"
cd ..
echo.

echo ========================================
echo DIAGNOSTIC COMPLETE
echo ========================================
pause

