@echo off
echo ========================================
echo  Next.js Development Server
echo ========================================
echo.

echo [1/3] Cleaning build cache...
if exist .next rmdir /s /q .next
if exist node_modules\.cache rmdir /s /q node_modules\.cache
echo ✓ Cache cleared
echo.

echo [2/3] Checking dependencies...
if not exist node_modules (
    echo Installing dependencies...
    call npm install
) else (
    echo ✓ Dependencies already installed
)
echo.

echo [3/3] Starting development server...
echo.
echo  Frontend will be available at:
echo  http://localhost:3002
echo.
echo  Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

npm run dev

