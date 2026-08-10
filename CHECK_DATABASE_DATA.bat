@echo off
echo ========================================
echo Checking Database Data
echo ========================================
echo.

echo 1. Checking PostgreSQL data...
echo ========================================
docker exec -it oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) as total_records FROM production_data;"
echo.

echo 2. Checking if Rig Alpha data exists...
echo ========================================
docker exec -it oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT rig_name, COUNT(*) as records FROM production_data GROUP BY rig_name;"
echo.

echo 3. Checking recent production data for Rig Alpha...
echo ========================================
docker exec -it oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT timestamp, rig_name, production_rate FROM production_data WHERE rig_name = 'Rig Alpha' ORDER BY timestamp DESC LIMIT 5;"
echo.

echo 4. Checking Neo4j data...
echo ========================================
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY type"
echo.

echo 5. Checking if Rig Alpha exists in Neo4j...
echo ========================================
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (r:Rig {name: 'Rig Alpha'}) RETURN r.name, r.location"
echo.

echo ========================================
echo Analysis:
echo ========================================
echo.
echo If you see "0 records" or empty results:
echo   - The databases are connected but NOT seeded with data
echo   - Run: SEED_DATABASES.bat
echo.
echo If you see data:
echo   - The issue is in the query processing logic
echo   - Check backend logs for errors
echo.
pause

