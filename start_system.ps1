# Start the Intelligent Oilfield Insight Platform

Write-Host "Starting Intelligent Oilfield Insight Platform..." -ForegroundColor Green

# Start databases
Write-Host "Starting databases..." -ForegroundColor Cyan
docker-compose up -d postgres neo4j qdrant minio

# Wait for databases to be ready (Neo4j needs extra time)
Write-Host "Waiting for databases to initialize (30 seconds)..." -ForegroundColor Yellow
Write-Host "  - PostgreSQL, Qdrant, MinIO: ~10 seconds" -ForegroundColor Gray
Write-Host "  - Neo4j: ~30 seconds (loading plugins)" -ForegroundColor Gray
Start-Sleep -Seconds 30

# Verify Neo4j is running
Write-Host "Verifying Neo4j status..." -ForegroundColor Cyan
$neo4jStatus = docker ps --filter "name=oilfield-neo4j" --format "{{.Status}}"
if ($neo4jStatus -match "Up") {
    Write-Host "  Neo4j: Running" -ForegroundColor Green
}
else {
    Write-Host "  Neo4j: Not running - attempting restart..." -ForegroundColor Yellow
    docker rm -f oilfield-neo4j
    docker-compose up -d neo4j
    Start-Sleep -Seconds 30
}

# Start backend in a new window
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Start frontend in a new window
Write-Host "Starting frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host "System startup initiated!" -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend will be available at: http://localhost:3002" -ForegroundColor White
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

