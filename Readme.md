# Idea2Image — Prototype

This repository contains Idea2Image, an application that builds optimized image-generation prompts from structured scene descriptions and optional LLM refinements.

Full, detailed documentation is available in the `docs/` folder. Start with `docs/setup.md` to get running quickly.

## Quickstart
1. Clone repo
2. Copy `.env.example` to `.env` and add `OPENAI_API_KEY`
3. Create a virtual environment and install:

```bash
pip install -e ".[dev]"
```

Windows users: `make` is not required — a PowerShell helper `dev.ps1` replicates the Makefile targets. Example:

```powershell
# install dev deps
.\dev.ps1 -Task dev-install
# run app
.\dev.ps1 -Task run
```

More details: see the `docs/` directory (architecture, usage, testing, deployment and developer guidelines).
# Idea2Image — Prototype

## Quickstart
1. Clone repo
2. Copy `.env.example` to `.env` and add `OPENAI_API_KEY`
3. Create a virtual environment and install:
