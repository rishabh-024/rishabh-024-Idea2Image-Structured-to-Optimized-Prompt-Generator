# Testing

This document describes how to run and extend the test suite.

Run tests locally

```powershell
.\dev.ps1 -Task test
# or
pytest tests/ -v
```

Run tests with coverage report

```powershell
.\dev.ps1 -Task test-cov
# or
pytest tests/ -v --cov=app --cov-report=html
```

Test guidelines
- Keep unit tests small and focused.
- Avoid network calls in unit tests; mock external APIs such as OpenAI.
- Use fixtures in `tests/conftest.py` to reuse common test setup.

Adding tests
1. Create a new test file `tests/test_new_feature.py`.
2. Use `pytest` style asserts.
3. Run `pytest -q` and ensure tests pass before submitting PR.

CI integration
- Configure your CI (GitHub Actions, GitLab CI) to create a Python environment, install dev dependencies and run `pytest --cov`.
