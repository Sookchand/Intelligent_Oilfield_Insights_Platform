@echo off
echo Testing Query Validator...
cd backend
call ..\venv\Scripts\activate.bat
python test_validator.py
pause

