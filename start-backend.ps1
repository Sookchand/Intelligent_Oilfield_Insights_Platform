Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kill old process
Write-Host "Checking for existing backend process..." -ForegroundColor Yellow
$existing = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($existing) {
    $pid = $existing.OwningProcess
    Write-Host "Killing existing process (PID: $pid)..." -ForegroundColor Yellow
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "✅ Old process killed" -ForegroundColor Green
} else {
    Write-Host "✅ No existing process found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting backend..." -ForegroundColor Yellow
Write-Host ""

# Change to backend directory
Set-Location -Path "$PSScriptRoot\backend"

# Start the backend
python main.py

Write-Host ""
Write-Host "Backend stopped." -ForegroundColor Red
Read-Host "Press Enter to exit"

