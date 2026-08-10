@echo off
echo ================================================================================
echo RUNNING INTEGRATION TESTS - Graph Engine Routing
echo ================================================================================
echo.
echo Testing:
echo   - Forecast query routing
echo   - AI routing exclusions
echo   - Multi-agent orchestration
echo   - Forecasting module integration
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run integration tests
cd tests
python test_graph_engine_integration.py

REM Return to root
cd ..

echo.
pause

