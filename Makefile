.PHONY: install run test

install:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt || .\\venv\\Scripts\\pip.exe install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q
