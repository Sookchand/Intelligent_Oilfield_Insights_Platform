Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESTARTING BACKEND WITH UPDATED CODE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Stopping any running Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Step 2: Starting backend with updated code..." -ForegroundColor Yellow
Set-Location backend
& ..\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Backend starting on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python main.py

