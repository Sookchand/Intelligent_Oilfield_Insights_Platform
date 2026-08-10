# Quick System Status Check
Write-Host "🔍 Checking System Status..." -ForegroundColor Cyan
Write-Host ""

# Check Backend (Port 8000)
Write-Host "Backend (Port 8000):" -ForegroundColor Yellow
try {
    $backend = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($backend) {
        Write-Host "  ✅ Backend is RUNNING on port 8000" -ForegroundColor Green
        Write-Host "  URL: http://localhost:8000" -ForegroundColor Gray
    } else {
        Write-Host "  ❌ Backend is NOT running" -ForegroundColor Red
        Write-Host "  Start with: cd backend; python main.py" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Backend is NOT running" -ForegroundColor Red
}
Write-Host ""

# Check Frontend (Port 3002)
Write-Host "Frontend (Port 3002):" -ForegroundColor Yellow
try {
    $frontend = Get-NetTCPConnection -LocalPort 3002 -State Listen -ErrorAction SilentlyContinue
    if ($frontend) {
        Write-Host "  ✅ Frontend is RUNNING on port 3002" -ForegroundColor Green
        Write-Host "  URL: http://localhost:3002" -ForegroundColor Gray
    } else {
        Write-Host "  ❌ Frontend is NOT running" -ForegroundColor Red
        Write-Host "  Start with: cd frontend; npm run dev" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Frontend is NOT running" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($backend -and $frontend) {
    Write-Host "✅ SYSTEM IS READY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Open: http://localhost:3002" -ForegroundColor White
    Write-Host "2. Test query: 'show me faulty equipment at Rig Alpha'" -ForegroundColor White
    Write-Host "3. Check explainability: http://localhost:3002/explainability" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: Database connection errors are normal if using mock data!" -ForegroundColor Gray
} elseif ($backend -and -not $frontend) {
    Write-Host "⚠️  Backend is running, but frontend is not" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Start frontend with:" -ForegroundColor Yellow
    Write-Host "  cd frontend" -ForegroundColor White
    Write-Host "  npm run dev" -ForegroundColor White
} elseif ($frontend -and -not $backend) {
    Write-Host "⚠️  Frontend is running, but backend is not" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Start backend with:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  python main.py" -ForegroundColor White
} else {
    Write-Host "❌ Neither backend nor frontend is running" -ForegroundColor Red
    Write-Host ""
    Write-Host "Start backend:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Then start frontend (in NEW terminal):" -ForegroundColor Yellow
    Write-Host "  cd frontend" -ForegroundColor White
    Write-Host "  npm run dev" -ForegroundColor White
}

