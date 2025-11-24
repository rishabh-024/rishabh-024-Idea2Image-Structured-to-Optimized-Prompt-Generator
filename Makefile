.PHONY: help install dev-install run test test-cov lint format clean docker-build docker-run

PYTHON := python
PIP := pip
PYTHON_VERSION := 3.8

help:
	@echo "Idea2Image - Development Tasks"
	@echo ""
	@echo "Available targets:"
	@echo "  install        - Install dependencies"
	@echo "  dev-install    - Install with dev dependencies"
	@echo "  run            - Run the application"
	@echo "  test           - Run tests"
	@echo "  test-cov       - Run tests with coverage"
	@echo "  lint           - Run code linters"
	@echo "  format         - Format code with black and isort"
	@echo "  clean          - Clean cache and build files"
	@echo "  docker-build   - Build Docker image"
	@echo "  docker-run     - Run Docker container"
	@echo "  setup          - Setup development environment"

install:
	$(PIP) install -r requirements.txt

dev-install:
	$(PIP) install -e ".[dev]"

run:
	$(PYTHON) -m app.ui

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=html

lint:
	flake8 app/ tests/
	mypy app/ --ignore-missing-imports

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/

docker-build:
	docker build -t idea2image:latest .

docker-run:
	docker run -p 7860:7860 -e OPENAI_API_KEY=${OPENAI_API_KEY} idea2image:latest

setup: clean
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  - On Windows: venv\\Scripts\\activate"
	@echo "  - On macOS/Linux: source venv/bin/activate"
	@echo "Then run: make dev-install"

release-check: clean lint test
	@echo "✓ All checks passed!"

.DEFAULT_GOAL := help
