$ErrorActionPreference = 'Stop'
Write-Host 'Creating virtual environment...'
python -m venv .venv
& .\.venv\Scripts\Activate.ps1

Write-Host 'Installing dependencies...'
pip install --upgrade pip
pip install -r requirements.txt

Write-Host 'Initializing database...'
python -m src.fair_evaluator.db_init

Write-Host 'Starting FastAPI server at http://localhost:8000/'
uvicorn src.fair_evaluator.main:app --reload --port 8000
