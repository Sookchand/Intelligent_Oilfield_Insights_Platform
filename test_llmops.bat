@echo off
echo ========================================
echo Testing LLMOps Integration
echo ========================================
echo.

echo [1/3] Checking LangSmith configuration...
echo ----------------------------------------
call venv\Scripts\activate
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); enabled = os.getenv('LANGCHAIN_TRACING_V2', 'false').lower() == 'true'; api_key = os.getenv('LANGCHAIN_API_KEY', ''); has_key = api_key and api_key != 'your-langsmith-api-key-here'; print('✅ LangSmith Tracing:', 'ENABLED' if enabled else 'DISABLED'); print('✅ API Key:', 'CONFIGURED' if has_key else 'NOT CONFIGURED'); print(); print('Status:', 'READY' if (enabled and has_key) else 'NEEDS SETUP'); print(); print('To enable:'); print('1. Sign up at https://smith.langchain.com'); print('2. Get API key from Settings → API Keys'); print('3. Add to .env: LANGCHAIN_API_KEY=your-key-here'); print('4. Restart backend')"
cd ..
echo.

echo [2/3] Testing metrics module...
echo ----------------------------------------
cd backend
python -c "from llmops.metrics import LLMMetrics, OilfieldLLMMetrics; metrics = LLMMetrics(); print('✅ LLMMetrics module loaded'); print('✅ OilfieldLLMMetrics module loaded'); print(); print('Available metrics:'); print('- Query latency tracking'); print('- Token usage tracking'); print('- Cost tracking'); print('- Numerical accuracy'); print('- Entity accuracy'); print('- Hallucination detection')"
cd ..
echo.

echo [3/3] Checking backend health...
echo ----------------------------------------
echo Starting backend in background...
start /B cmd /c "cd backend && ..\venv\Scripts\activate && python main.py > ..\backend_test.log 2>&1"
timeout /t 5 /nobreak > nul
echo.
echo Checking health endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo ========================================
echo LLMOps Test Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Check LANGSMITH_SETUP.md for API key setup
echo 2. View full roadmap in LLMOPS_ROADMAP.md
echo 3. Restart backend to see LangSmith status
echo.
echo Backend log: backend_test.log
echo.
pause

