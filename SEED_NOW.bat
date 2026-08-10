@echo off
echo ========================================
echo SEEDING DATABASES NOW
echo ========================================
echo.

echo [1/2] Seeding Neo4j Graph Database...
echo ========================================
type data\seed_graph.cypher | docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass
echo.
echo ✅ Neo4j seeded
echo.

echo [2/2] Seeding PostgreSQL Database...
echo ========================================
type data\seed_sql.sql | docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production
echo.
echo ✅ PostgreSQL seeded
echo.

echo ========================================
echo VERIFICATION
echo ========================================
echo.
echo Checking Neo4j nodes:
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY type"
echo.

echo Checking Well W-12 sensors:
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (w:Well {name: 'Well W-12'})-[:HAS_SENSOR]->(s:Sensor) RETURN s.sensor_id, s.sensor_type"
echo.

echo ========================================
echo ✅ SEEDING COMPLETE!
echo ========================================
echo.
echo Next Steps:
echo 1. Restart backend: Ctrl+C in backend terminal, then: python main.py
echo 2. Refresh frontend: Press F5 in browser
echo 3. Try query: "What is the name and type of gauge at Well W-12?"
echo.
echo Expected Answer: "Pressure Gauge G-40"
echo.
pause

