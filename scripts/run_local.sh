#!/usr/bin/env bash
set -euo pipefail

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Initializing database..."
python -m src.fair_evaluator.db_init

echo "Starting FastAPI server at http://localhost:8000/"
uvicorn src.fair_evaluator.main:app --reload --port 8000
