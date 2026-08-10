@echo off
echo ========================================
echo Starting Database Services
echo ========================================
echo.

echo Checking if Docker is running...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo Or start Docker Desktop if already installed
    pause
    exit /b 1
)

echo Docker found!
echo.

echo Starting database containers...
echo This will start:
echo   - PostgreSQL on port 5433
echo   - Neo4j on ports 7474 (browser) and 7687 (bolt)
echo   - Qdrant on port 6333
echo   - MinIO on ports 9002 (API) and 9003 (console)
echo.

docker-compose up -d postgres neo4j qdrant minio

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start containers
    echo.
    echo Try running: docker-compose down
    echo Then run this script again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Waiting for databases to initialize...
echo ========================================
echo.
echo This may take 30-60 seconds...
timeout /t 30 /nobreak

echo.
echo ========================================
echo Checking database health...
echo ========================================
echo.

docker-compose ps

echo.
echo ========================================
echo Database URLs:
echo ========================================
echo.
echo PostgreSQL:
echo   Host: localhost:5433
echo   Database: oilfield_production
echo   User: oilfield_user
echo   Password: oilfield_pass
echo.
echo Neo4j Browser:
echo   URL: http://localhost:7474
echo   User: neo4j
echo   Password: oilfield_neo4j_pass
echo.
echo Qdrant:
echo   URL: http://localhost:6333
echo.
echo MinIO Console:
echo   URL: http://localhost:9003
echo   User: minio_admin
echo   Password: minio_admin_pass
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Restart your backend (Ctrl+C in backend terminal, then run again)
echo 2. The database connectivity should now show GREEN
echo 3. Test a query on the dashboard
echo.
echo To stop databases: docker-compose down
echo To view logs: docker-compose logs -f
echo.
pause

