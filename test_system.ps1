# System Testing Script
# Run this after starting backend and frontend

Write-Host "🧪 Testing Intelligent Oilfield Insight Platform..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Backend Health
Write-Host "Test 1: Backend Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is running on port 5001" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend is NOT running on port 5001" -ForegroundColor Red
    Write-Host "   Start it with: cd backend; python main.py" -ForegroundColor Yellow
}
Write-Host ""

# Test 2: Frontend
Write-Host "Test 2: Frontend Check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3002" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running on port 3002" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend is NOT running on port 3002" -ForegroundColor Red
    Write-Host "   Start it with: cd frontend; npm run dev" -ForegroundColor Yellow
}
Write-Host ""

# Test 3: PostgreSQL
Write-Host "Test 3: PostgreSQL Check..." -ForegroundColor Yellow
try {
    $pgService = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($pgService -and $pgService.Status -eq "Running") {
        Write-Host "✅ PostgreSQL is running" -ForegroundColor Green
    } else {
        Write-Host "⚠️  PostgreSQL service not found or not running" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not check PostgreSQL status" -ForegroundColor Yellow
}
Write-Host ""

# Test 4: Neo4j
Write-Host "Test 4: Neo4j Check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7474" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Neo4j is accessible on port 7474" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Neo4j is NOT accessible on port 7474" -ForegroundColor Red
    Write-Host "   Start Neo4j Desktop application" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: API Query Test
Write-Host "Test 5: API Query Test..." -ForegroundColor Yellow
try {
    $body = @{
        query = "show me faulty equipment at Rig Alpha"
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/query" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -UseBasicParsing `
        -TimeoutSec 10

    if ($response.StatusCode -eq 200) {
        $result = $response.Content | ConvertFrom-Json
        Write-Host "✅ API query successful" -ForegroundColor Green
        Write-Host "   Answer preview: $($result.answer.Substring(0, [Math]::Min(100, $result.answer.Length)))..." -ForegroundColor Gray
        Write-Host "   Confidence: $($result.confidence)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ API query failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 Test Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open browser: http://localhost:3002" -ForegroundColor White
Write-Host "2. Test AI query: 'show me faulty equipment at Rig Alpha'" -ForegroundColor White
Write-Host "3. Go to explainability page: http://localhost:3002/explainability" -ForegroundColor White
Write-Host "4. Review MASTER_DEMO_GUIDE.md for demo flow" -ForegroundColor White
Write-Host ""
Write-Host "🚀 System is ready for demo!" -ForegroundColor Green

