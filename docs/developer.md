# Developer Guide

This document contains guidance for contributors and maintainers: code structure, style and how to extend the project.

Repository layout (important files)
- `app/` — core Python package. Key modules:
  - `app/ui.py` — Gradio UI and orchestration
  - `app/prompt_engine.py` — prompt template builder and LLM refinements
  - `app/retrieval.py` — prompt bank, embeddings and FAISS index
  - `app/output_formatter.py` — packages prompt outputs
  - `app/utils.py` — helpers and environment utilities

- `data/` — sample prompts and any auxiliary data
- `models/` — reserved for model artifacts (not committed)
- `tests/` — pytest test suite

Coding standards
- Python: follow PEP 8, use type hints on public functions and methods.
- Formatting: run `black` and `isort` (or use `.\dev.ps1 -Task format`).
- Linting: `flake8` and `mypy` configured in `setup.cfg` / `pyproject.toml`.

Adding a new prompt to the bank
1. Add new entry to `data/sample_prompts.json` using the existing schema.
2. If you add many prompts, re-generate embeddings in `app/retrieval.py` or include a serialized index in `models/`.

Extending the retrieval backend
- The retrieval layer separates embedding computation and the search backend. To switch to a different vector DB:
  - Replace the FAISS index building in `PromptRetrieval._build_index()` with the target provider code.
  - Keep method `retrieve(query, k)` signature consistent so `app/ui.py` and tests continue to work.

OpenAI compatibility notes
- The `prompt_engine` contains logic to call the OpenAI chat completions API using a compatibility wrapper: it tries the newer `client.chat.completions.create()` pattern first and falls back to older `client.ChatCompletion.create()` calls when needed.

Testing and CI
- Write unit tests in `tests/` and make sure they run locally with `pytest tests/ -v`.
- Tests that call external services (OpenAI) should be either mocked or use recorded responses (vcrpy) to avoid network dependence in CI.

Developer workflow example
```bash
# create branch
git checkout -b feat/new-style
# run tests and lint
.\dev.ps1 -Task test
.\dev.ps1 -Task lint
# run UI locally for manual testing
.\dev.ps1 -Task run
```
