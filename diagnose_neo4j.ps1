Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Neo4j Diagnostic Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if container exists
Write-Host "1. Checking if Neo4j container exists..." -ForegroundColor Yellow
docker ps -a --filter "name=oilfield-neo4j" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

# Check container logs
Write-Host "2. Neo4j Container Logs (last 50 lines):" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Gray
docker logs oilfield-neo4j --tail 50
Write-Host ""

# Check if ports are listening
Write-Host "3. Checking if ports 7474 and 7687 are listening..." -ForegroundColor Yellow
$port7474 = Get-NetTCPConnection -LocalPort 7474 -State Listen -ErrorAction SilentlyContinue
$port7687 = Get-NetTCPConnection -LocalPort 7687 -State Listen -ErrorAction SilentlyContinue

if ($port7474) {
    Write-Host "  ✅ Port 7474 (HTTP) is listening" -ForegroundColor Green
} else {
    Write-Host "  ❌ Port 7474 (HTTP) is NOT listening" -ForegroundColor Red
}

if ($port7687) {
    Write-Host "  ✅ Port 7687 (Bolt) is listening" -ForegroundColor Green
} else {
    Write-Host "  ❌ Port 7687 (Bolt) is NOT listening" -ForegroundColor Red
}
Write-Host ""

# Test HTTP endpoint
Write-Host "4. Testing HTTP endpoint (7474)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7474" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✅ HTTP endpoint is responding (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  ❌ HTTP endpoint is NOT responding: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Check Docker container inspect
Write-Host "5. Container Details:" -ForegroundColor Yellow
docker inspect oilfield-neo4j --format "{{.State.Status}} - {{.State.Health.Status}}" 2>$null
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Recommended Actions:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not $port7687) {
    Write-Host "Neo4j Bolt port (7687) is not listening." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try these steps:" -ForegroundColor White
    Write-Host "  1. docker restart oilfield-neo4j" -ForegroundColor Gray
    Write-Host "  2. Wait 60 seconds" -ForegroundColor Gray
    Write-Host "  3. Run this script again" -ForegroundColor Gray
    Write-Host ""
    Write-Host "If that doesn't work:" -ForegroundColor White
    Write-Host "  1. docker-compose down" -ForegroundColor Gray
    Write-Host "  2. docker volume rm intelligentoilfieldinsightplatform_neo4j_data" -ForegroundColor Gray
    Write-Host "  3. docker-compose up -d neo4j" -ForegroundColor Gray
    Write-Host "  4. Wait 60 seconds" -ForegroundColor Gray
} else {
    Write-Host "✅ Neo4j appears to be running correctly!" -ForegroundColor Green
    Write-Host ""
    Write-Host "If backend still can't connect:" -ForegroundColor White
    Write-Host "  1. Restart the backend (Ctrl+C, then python main.py)" -ForegroundColor Gray
    Write-Host "  2. Check backend .env file has: NEO4J_URI=bolt://localhost:7687" -ForegroundColor Gray
}
Write-Host ""

