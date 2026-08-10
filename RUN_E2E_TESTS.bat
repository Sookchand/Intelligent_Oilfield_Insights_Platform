@echo off
echo ================================================================================
echo RUNNING END-TO-END TESTS - Complete System
echo ================================================================================
echo.
echo Prerequisites:
echo   1. Backend must be running: cd backend ^&^& python main.py
echo   2. Databases must be running: docker-compose up -d
echo.
echo Press Ctrl+C to cancel if prerequisites are not met.
echo.
pause

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run end-to-end tests
cd tests
python test_system_end_to_end.py

REM Return to root
cd ..

echo.
pause

