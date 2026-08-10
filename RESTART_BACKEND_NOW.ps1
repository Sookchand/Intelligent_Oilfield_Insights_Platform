# Restart Backend Script
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "Restarting Backend with New Fixes" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 79) -ForegroundColor Cyan

# Kill any existing Python processes running on port 8000
Write-Host "`n[1/3] Stopping existing backend..." -ForegroundColor Yellow
$processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($processes) {
    foreach ($proc in $processes) {
        Write-Host "  Killing process $proc" -ForegroundColor Gray
        Stop-Process -Id $proc -Force -ErrorAction SilentlyContinue
    }
    Write-Host "  ✓ Stopped existing backend" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "  No existing backend found" -ForegroundColor Gray
}

# Activate virtual environment and start backend
Write-Host "`n[2/3] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

Write-Host "`n[3/3] Starting backend with new fixes..." -ForegroundColor Yellow
Write-Host "  - PostgreSQL parameter conversion (✓)" -ForegroundColor Gray
Write-Host "  - Intelligent result formatting (✓)" -ForegroundColor Gray
Write-Host ""

# Change to backend directory and start
Set-Location backend
python main.py

