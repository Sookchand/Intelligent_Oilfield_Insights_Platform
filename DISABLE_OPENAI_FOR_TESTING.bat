@echo off
REM Quick fix: Disable OpenAI to use fast fallback mode
REM This will make queries faster but with lower confidence

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║     DISABLE OPENAI - USE FALLBACK MODE                             ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo This will:
echo   - Comment out OPENAI_API_KEY in .env
echo   - Backend will use fast rule-based queries
echo   - Response time: 1-5s (instead of 25s+)
echo   - Confidence: 60-75%% (instead of 30%%)
echo.
echo You can re-enable OpenAI later by adding a real API key.
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 1: BACKING UP .env FILE
echo ════════════════════════════════════════════════════════════════════
echo.

if exist .env (
    copy .env .env.backup >nul 2>&1
    echo ✅ Backup created: .env.backup
) else (
    echo ❌ ERROR: .env file not found
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 2: UPDATING .env FILE
echo ════════════════════════════════════════════════════════════════════
echo.

REM Create temporary file with updated content
(
    for /f "delims=" %%i in (.env) do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        if "!line:~0,15!"=="OPENAI_API_KEY=" (
            echo # OPENAI_API_KEY=sk-your-api-key-here  # Disabled for testing
        ) else (
            echo !line!
        )
        endlocal
    )
) > .env.tmp

REM Replace original with updated
move /y .env.tmp .env >nul 2>&1

echo ✅ OpenAI API key commented out in .env
echo.

echo.
echo ════════════════════════════════════════════════════════════════════
echo STEP 3: VERIFICATION
echo ════════════════════════════════════════════════════════════════════
echo.

findstr /C:"# OPENAI_API_KEY" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Verified: OpenAI is now disabled
) else (
    echo ⚠️  Warning: Could not verify change
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo NEXT STEPS
echo ════════════════════════════════════════════════════════════════════
echo.
echo 1. Restart your backend:
echo    - Press Ctrl+C in backend terminal
echo    - Run: python main.py
echo.
echo 2. Look for this message in backend logs:
echo    "⚠️ OpenAI API key not found or invalid"
echo    "INFO: Using fallback query generation"
echo.
echo 3. Run tests:
echo    VALIDATE_PRODUCTION_READY.bat
echo.
echo Expected results:
echo    ✅ Response time: ^< 5s (much faster!)
echo    ⚠️  Confidence: 60-75%% (lower but acceptable)
echo    ✅ Overall score: 75-85%%
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo To re-enable OpenAI later:
echo   1. Get API key from https://platform.openai.com/api-keys
echo   2. Edit .env and uncomment OPENAI_API_KEY line
echo   3. Replace with your real key
echo   4. Restart backend
echo.
echo Backup saved as: .env.backup
echo.
pause

