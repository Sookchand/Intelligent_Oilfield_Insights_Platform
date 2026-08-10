@echo off
echo ========================================
echo Starting Intelligent Oilfield Platform
echo (Local Development Mode)
echo ========================================
echo.

REM Step 1: Check Docker
echo [1/5] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)
echo ✅ Docker is available
echo.

REM Step 2: Start Database Containers Only
echo [2/5] Starting Database Containers...
echo     - PostgreSQL (port 5433)
echo     - Neo4j (port 7687, 7474)
echo     - Qdrant (port 6333)
echo     - MinIO (port 9002, 9003)
echo.
docker-compose up -d postgres neo4j qdrant minio
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to start database containers
    pause
    exit /b 1
)
echo ✅ Database containers started
echo.

REM Step 3: Wait for databases to be healthy
echo [3/5] Waiting for databases to initialize (30 seconds)...
timeout /t 30 /nobreak >nul
echo.

REM Step 4: Seed databases if needed
echo [4/5] Checking if databases need seeding...
docker exec oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) FROM production_data" 2>nul | findstr "13" >nul
if %errorlevel% neq 0 (
    echo Seeding PostgreSQL...
    docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production < data\seed_sql.sql
)

docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n:Rig {name: 'Rig Alpha'}) RETURN n LIMIT 1" 2>nul | findstr "Rig Alpha" >nul
if %errorlevel% neq 0 (
    echo Seeding Neo4j...
    docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
)
echo ✅ Databases ready
echo.

REM Step 5: Start Backend and Frontend
echo [5/5] Starting Backend and Frontend...
echo.
echo Opening 2 new windows:
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:3001
echo.

REM Start Backend in new window
start "Oilfield Backend" cmd /k "cd /d %~dp0backend && ..\venv\Scripts\activate && echo Starting Backend Server... && echo. && uvicorn main:app --reload"

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Start Frontend in new window
start "Oilfield Frontend" cmd /k "cd /d %~dp0frontend && echo Starting Frontend Server... && echo. && echo Please wait 10-15 seconds for frontend to compile... && echo. && npm run dev"

echo.
echo ========================================
echo Platform Starting!
echo ========================================
echo.
echo Two new windows have opened:
echo   1. Backend Server (FastAPI)
echo   2. Frontend Server (Next.js)
echo.
echo Wait 30-60 seconds for everything to start, then visit:
echo   👉 http://localhost:3001
echo.
echo All 4 databases should show "Connected"
echo.
echo To stop everything:
echo   - Close the Backend and Frontend windows
echo   - Run: docker-compose down
echo.
pause

