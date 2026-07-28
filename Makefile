.PHONY: install test run api dashboard data

install:
	python3.12 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -r requirements-dev.txt
	cd apps/dashboard && npm install

test:
	.venv/bin/python -m pytest
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .
	.venv/bin/mypy packages apps
	cd apps/dashboard && npm run build

run:
	@sh -c '.venv/bin/uvicorn apps.api.main:app --reload & api_pid=$$!; trap "kill $$api_pid" EXIT INT TERM; cd apps/dashboard && npm run dev'

data:
	.venv/bin/python scripts/generate_synthetic_data.py
