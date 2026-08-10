#!/usr/bin/env pwsh
# Seed PostgreSQL Database with Production Data

Write-Host "🌱 Seeding PostgreSQL Database..." -ForegroundColor Cyan

# Check if Docker is running
$dockerRunning = docker ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if postgres container is running
$postgresRunning = docker ps --filter "name=oilfield-postgres" --format "{{.Names}}"
if (-not $postgresRunning) {
    Write-Host "❌ PostgreSQL container is not running." -ForegroundColor Red
    Write-Host "Run: docker-compose up -d postgres" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ PostgreSQL container is running" -ForegroundColor Green

# Load seed data
Write-Host "`n📊 Loading seed data into PostgreSQL..." -ForegroundColor Cyan

$seedFile = "data\seed_sql.sql"
if (-not (Test-Path $seedFile)) {
    Write-Host "❌ Seed file not found: $seedFile" -ForegroundColor Red
    exit 1
}

# Execute seed file
Get-Content $seedFile | docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database seeded successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to seed database" -ForegroundColor Red
    exit 1
}

# Verify data was loaded
Write-Host "`n🔍 Verifying data..." -ForegroundColor Cyan

$verifyQuery = "SELECT COUNT(*) as count FROM production_data;"
$count = docker exec -i oilfield-postgres psql -U oilfield_user -d oilfield_production -t -c $verifyQuery

Write-Host "✓ Production records loaded: $($count.Trim())" -ForegroundColor Green

Write-Host "`n✅ Database seeding complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Restart the backend: cd backend && uvicorn main:app --reload" -ForegroundColor White
Write-Host "2. Test the query: 'Why is production dropping at Rig Alpha?'" -ForegroundColor White

