@echo off
echo ========================================
echo Re-seeding All Databases
echo ========================================
echo.

echo This will add sample data to PostgreSQL and Neo4j
echo.
pause

echo.
echo [1/4] Seeding PostgreSQL...
echo ========================================
docker cp data\seed_sql.sql oilfield-postgres:/tmp/seed_sql.sql
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -f /tmp/seed_sql.sql
echo.

echo [2/4] Seeding Neo4j...
echo ========================================
docker cp data\seed_graph.cypher oilfield-neo4j:/tmp/seed_graph.cypher
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass -f /tmp/seed_graph.cypher
echo.

echo [3/4] Verifying PostgreSQL data...
echo ========================================
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) as total_records FROM production_data;"
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT DISTINCT rig_name FROM production_data LIMIT 5;"
echo.

echo [4/4] Verifying Neo4j data...
echo ========================================
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN labels(n)[0] as type, count(n) as count"
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (r:Rig) RETURN r.name LIMIT 5"
echo.

echo ========================================
echo Seeding Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. The databases now have sample data
echo 2. Restart your backend (Ctrl+C in backend terminal, then: python main.py)
echo 3. Refresh the frontend (F5 in browser)
echo 4. Try query: "why is production dropping at rig alpha?"
echo.
echo You should now get a detailed answer with high confidence!
echo.
pause

