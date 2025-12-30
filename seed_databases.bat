@echo off
echo ========================================
echo Seeding Databases with Sample Data
echo ========================================
echo.

echo 1. Seeding Neo4j Graph Database...
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass -f /var/lib/neo4j/import/seed_graph.cypher
if errorlevel 1 (
    echo    ❌ Failed to seed Neo4j
) else (
    echo    ✅ Neo4j seeded successfully
)

echo.
echo 2. Verifying PostgreSQL data...
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) FROM production_data;"

echo.
echo ========================================
echo Database Seeding Complete!
echo ========================================
echo.
echo You can now restart the backend and try queries like:
echo   "Why is production dropping at Rig Alpha?"
echo   "Show me faulty equipment at Rig Alpha"
echo   "What incidents occurred in the Permian Basin?"
echo.
pause

