@echo off
echo ================================================================================
echo RUNNING UNIT TESTS - Query Routing Fixes
echo ================================================================================
echo.
echo Testing:
echo   - Parser intent detection
echo   - Entity extraction
echo   - Execution plan creation
echo   - Priority-based routing
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run unit tests
cd tests
python test_query_routing_fixes.py

REM Return to root
cd ..

echo.
pause

