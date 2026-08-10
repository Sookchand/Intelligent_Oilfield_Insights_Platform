@echo off
echo ========================================
echo Resetting Frontend (Fixing CSS Issues)
echo ========================================
echo.

echo [1/4] Removing .next cache...
if exist .next (
    rmdir /s /q .next
    echo ✅ Cache cleared
) else (
    echo ℹ️  No cache to clear
)
echo.

echo [2/4] Removing node_modules...
if exist node_modules (
    echo This may take a minute...
    rmdir /s /q node_modules
    echo ✅ node_modules removed
) else (
    echo ℹ️  node_modules already removed
)
echo.

echo [3/4] Reinstalling dependencies...
echo This will take 1-2 minutes...
call npm install
if %errorlevel% neq 0 (
    echo ❌ ERROR: npm install failed
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

echo [4/4] Starting development server...
echo.
echo Frontend will start at http://localhost:3001
echo CSS should now load properly!
echo.
call npm run dev

