@echo off
echo Starting Local Fairs Evaluator (Windows)
set VENV=venv
if not exist %VENV% (
  echo Creating virtual environment...
  python -m venv %VENV%
)
call %VENV%\Scripts\activate.bat
echo Installing/updating dependencies (optional, but recommended)...
pip install --upgrade pip
pip install -r requirements.txt
echo Launching uvicorn...
uvicorn src.fair_evaluator.main:app --reload --port 8000
