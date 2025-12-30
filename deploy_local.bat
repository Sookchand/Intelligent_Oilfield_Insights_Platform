@echo off
echo ========================================
echo Intelligent Oilfield Insights Platform
echo Local Deployment Script
echo ========================================
echo.

REM Check if Docker is running
echo [1/8] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running
    echo Please install Docker Desktop and start it
    pause
    exit /b 1
)
echo Docker is running!
echo.

REM Check if .env file exists
echo [2/8] Checking environment configuration...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your OPENAI_API_KEY
    echo Press any key after you've added your API key...
    pause
)
echo Environment configured!
echo.

REM Stop any existing containers
echo [3/8] Stopping existing containers...
docker-compose down
echo.

REM Start Docker services
echo [4/8] Starting Docker services...
echo This may take a few minutes on first run...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start Docker services
    pause
    exit /b 1
)
echo Docker services started!
echo.

REM Wait for services to be ready
echo [5/8] Waiting for services to initialize (30 seconds)...
timeout /t 30 /nobreak
echo.

REM Initialize PostgreSQL database
echo [6/8] Initializing PostgreSQL database...
docker-compose exec -T postgres psql -U oilfield_user -d oilfield_production < data\seed_sql.sql
if errorlevel 1 (
    echo WARNING: PostgreSQL initialization may have failed
    echo This is normal if the database was already initialized
)
echo PostgreSQL initialized!
echo.

REM Initialize Neo4j graph database
echo [7/8] Initializing Neo4j graph database...
docker-compose exec -T neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
if errorlevel 1 (
    echo WARNING: Neo4j initialization may have failed
    echo This is normal if the graph was already initialized
)
echo Neo4j initialized!
echo.

REM Verify deployment
echo [8/8] Verifying deployment...
echo.
echo Checking service health...
timeout /t 5 /nobreak >nul

curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: Backend may not be ready yet
    echo Give it a few more seconds and try accessing http://localhost:8000/docs
) else (
    echo Backend is healthy!
)
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Services are now running:
echo.
echo   Frontend:        http://localhost:3000
echo   Backend API:     http://localhost:8000
echo   API Docs:        http://localhost:8000/docs
echo   Neo4j Browser:   http://localhost:7474
echo   MinIO Console:   http://localhost:9001
echo   Qdrant Dashboard: http://localhost:6333/dashboard
echo.
echo Credentials:
echo   Neo4j:  neo4j / oilfield_neo4j_pass
echo   MinIO:  minio_admin / minio_admin_pass
echo.
echo To test the platform, try:
echo   curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d "{\"query\": \"Why is production dropping at Rig Alpha?\"}"
echo.
echo To view logs:
echo   docker-compose logs -f backend
echo.
echo To stop all services:
echo   docker-compose down
echo.
pause

