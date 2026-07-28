.PHONY: install test run api dashboard data

install:
	python3.12 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt
	cd apps/dashboard && npm install

test:
	.venv/bin/python -m pytest
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .
	.venv/bin/mypy packages apps
	cd apps/dashboard && npm run build

run:
	@trap 'kill 0' INT TERM EXIT; .venv/bin/uvicorn apps.api.main:app --reload & cd apps/dashboard && npm run dev

data:
	.venv/bin/python scripts/generate_synthetic_data.py
