@echo off
REM Seed PostgreSQL Database with Production Data

echo.
echo ========================================
echo   Seeding PostgreSQL Database
echo ========================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [OK] Docker is running

REM Check if postgres container is running
docker ps --filter "name=oilfield-postgres" --format "{{.Names}}" | findstr "oilfield-postgres" >nul
if errorlevel 1 (
    echo [ERROR] PostgreSQL container is not running.
    echo Run: docker-compose up -d postgres
    pause
    exit /b 1
)

echo [OK] PostgreSQL container is running
echo.

REM Load seed data
echo Loading seed data into PostgreSQL...
echo.

type data\seed_sql.sql | docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to seed database
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Database seeded successfully!
echo.

REM Verify data was loaded
echo Verifying data...
docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production -t -c "SELECT COUNT(*) as count FROM production_data;"

echo.
echo ========================================
echo   Database Seeding Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Restart the backend (if running)
echo 2. Test query: "Why is production dropping at Rig Alpha?"
echo.
pause

