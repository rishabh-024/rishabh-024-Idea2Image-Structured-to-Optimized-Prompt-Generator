# CONTRIBUTING.md

Contributions are welcome! Please follow these guidelines.

## Code Style

- **PEP 8**: Follow Python style guidelines with 79-character line limit
- **Type Hints**: Add type hints to all functions
- **Docstrings**: Write comprehensive docstrings for all public functions
- **Logging**: Use logging instead of print statements

## Before Committing

1. **Format Code**
   ```bash
   black .
   isort .
   ```

2. **Run Linters**
   ```bash
   flake8 app/
   mypy app/
   ```

3. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

4. **Test Locally**
   ```bash
   python -m app.ui
   ```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Refactor"
- Example: "Add error handling for missing API keys"

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/feature-name`)
3. Commit changes with clear messages
4. Push to your fork
5. Open a pull request with description of changes

## Issues

- Search existing issues before creating new ones
- Provide reproducible examples when possible
- Include Python version, OS, and dependency versions

## Development Setup

```bash
git clone <your-fork>
cd idea2image
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
```

## Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_core.py

# With coverage
pytest --cov=app tests/

# Specific test
pytest tests/test_core.py::TestPromptEngine::test_build_template_basic
```

Thank you for contributing!
