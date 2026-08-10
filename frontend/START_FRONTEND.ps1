# PowerShell script to launch frontend in Command Prompt
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Starting Frontend in Command Prompt" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$frontendPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Opening Command Prompt window..." -ForegroundColor Yellow
Write-Host ""

# Launch Command Prompt with the batch file
Start-Process cmd.exe -ArgumentList "/k", "cd /d `"$frontendPath`" && start-dev.bat"

Write-Host "✓ Command Prompt window opened!" -ForegroundColor Green
Write-Host ""
Write-Host "The frontend server is starting in the new window." -ForegroundColor White
Write-Host "Once you see 'Ready in X.Xs', open your browser to:" -ForegroundColor White
Write-Host ""
Write-Host "  http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open the browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:3000"

