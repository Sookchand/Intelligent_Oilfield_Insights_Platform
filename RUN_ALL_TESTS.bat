@echo off
echo ================================================================================
echo RUNNING ALL TESTS - Query Routing Fixes
echo ================================================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run all tests
cd tests
python run_all_tests.py

REM Return to root
cd ..

echo.
echo ================================================================================
echo Tests complete!
echo ================================================================================
echo.
pause

