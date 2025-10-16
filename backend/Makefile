# ChargeChase Backend Makefile

.PHONY: help install test test-unit test-integration test-coverage run clean lint format

help:			## Show this help message
	@echo "ChargeChase Backend - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:		## Install dependencies
	pip install -r requirements.txt

test:			## Run all tests
	pytest

test-unit:		## Run unit tests only
	pytest -m unit

test-integration:	## Run integration tests only  
	pytest -m integration

test-coverage:		## Run tests with coverage report
	pytest --cov=app --cov-report=html --cov-report=term-missing

test-watch:		## Run tests in watch mode
	pytest -f

run:			## Start development server
	python -m app.main

run-uvicorn:		## Start with uvicorn (alternative)
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

db-upgrade:		## Run database migrations
	alembic upgrade head

db-downgrade:		## Downgrade database by one migration
	alembic downgrade -1

db-revision:		## Create new migration (use: make db-revision MESSAGE="description")
	alembic revision --autogenerate -m "$(MESSAGE)"

clean:			## Clean up generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f test_chargechase.db

lint:			## Run linting (if available)
	@echo "Linting not configured yet - add ruff or similar"

format:			## Format code (if available)
	@echo "Formatting not configured yet - add black or similar"

# Development helpers
deps-upgrade:		## Upgrade all dependencies
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

info:			## Show project info
	@echo "ChargeChase Backend"
	@echo "Python: $(shell python --version)"
	@echo "FastAPI app: app.main:app"
	@echo "Database URL: Check .env file"