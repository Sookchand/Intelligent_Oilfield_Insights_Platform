@echo off
echo Checking if databases have data...
echo.

echo PostgreSQL:
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) as production_records FROM production_data;" 2>nul
echo.

echo Neo4j:
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n) as total_nodes" 2>nul
echo.

pause

