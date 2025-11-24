# Setup

This document explains how to set up the project locally on Windows, macOS and Linux.

Prerequisites
- Python 3.10+ (the project was developed and tested on Python 3.10/3.11)
- Git
- (Optional) Docker and Docker Compose for containerized runs

1) Clone repository

```bash
git clone <your-repo-url>
cd Idea2Image
```

2) Create and activate virtual environment

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies

There are two options: use the `Makefile` (Unix) or the included `dev.ps1` helper (Windows), or install directly via pip.

Windows (recommended):
```powershell
# From project root with venv activated
.\dev.ps1 -Task dev-install
```

Unix / macOS:
```bash
pip install -e ".[dev]"
```

4) Configure API keys

Copy `.env.example` to `.env` and populate the `OPENAI_API_KEY`:

```powershell
Copy-Item .env.example .env
notepad .env
```

Or set the key in your session (temporary):

```powershell
$env:OPENAI_API_KEY = 'sk-...'
```

5) Run the application

```powershell
# Start the app (Gradio web UI)
.\dev.ps1 -Task run
```

6) Common troubleshooting
- If `make` is not available on Windows, use `dev.ps1` (already provided).
- If the server starts but doesn't respond, check firewall / binding and ensure `7860` is not blocked.
