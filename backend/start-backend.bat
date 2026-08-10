@echo off
echo Activating Python virtual environment...
call venv\Scripts\activate

echo Starting FastAPI Backend Server...
uvicorn main:app --reload

