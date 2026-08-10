@echo off
echo ========================================
echo Fixing Frontend Build Corruption
echo ========================================
echo.

cd frontend

echo Step 1: Stopping any running frontend processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Deleting corrupted .next folder...
if exist .next (
    rmdir /s /q .next
    echo ✅ Deleted .next folder
) else (
    echo ℹ️  .next folder doesn't exist
)

echo Step 3: Deleting node_modules/.cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo ✅ Deleted node_modules/.cache
)

echo Step 4: Rebuilding frontend...
call npm run build

echo.
echo ========================================
echo Frontend rebuild complete!
echo ========================================
echo.
echo Now run: cd frontend && npm run dev
echo.
pause

