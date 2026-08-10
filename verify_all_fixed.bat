@echo off
echo ========================================
echo FINAL VERIFICATION - ALL SYSTEMS
echo ========================================
echo.

echo [1/5] Loading Neo4j graph data...
echo ----------------------------------------
type data\seed_graph.cypher | docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass
echo.

echo [2/5] Verifying Neo4j data loaded...
echo ----------------------------------------
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN labels(n)[0] as type, count(*) as count ORDER BY type"
echo.

echo [3/5] Testing all database connections...
echo ----------------------------------------
call venv\Scripts\activate
cd backend
python -c "from database.connections import test_all_connections; import json; result = test_all_connections(); print(json.dumps(result, indent=2)); print('\n'); print('✅ PostgreSQL:', '✓' if result['postgres'] else '✗'); print('✅ Neo4j:', '✓' if result['neo4j'] else '✗'); print('✅ Qdrant:', '✓' if result['qdrant'] else '✗'); print('✅ MinIO:', '✓' if result['minio'] else '✗')"
cd ..
echo.

echo [4/5] Checking Docker containers...
echo ----------------------------------------
docker-compose ps
echo.

echo [5/5] Testing Neo4j query from Python...
echo ----------------------------------------
cd backend
python -c "from database.connections import get_neo4j_driver; driver = get_neo4j_driver(); session = driver.session(); result = session.run('MATCH (r:Rig)-[:HAS_WELL]->(w:Well)-[:HAS_SENSOR]->(s:Sensor {status: \"FAULTY\"}) RETURN r.name as rig, w.name as well, s.name as sensor LIMIT 1'); record = result.single(); print(f'✅ Found faulty sensor: {record[\"sensor\"]} on {record[\"well\"]} at {record[\"rig\"]}') if record else print('⚠️ No faulty sensors found'); session.close(); driver.close()"
cd ..
echo.

echo ========================================
echo VERIFICATION COMPLETE!
echo ========================================
echo.
echo If all checks passed, you can now:
echo 1. Start the backend: cd backend ^& python main.py
echo 2. Test queries on the main page
echo.
pause

