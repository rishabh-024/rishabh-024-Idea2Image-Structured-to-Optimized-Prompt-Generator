# Quick Start Guide

Get Idea2Image running in 3 minutes.

## Step 1: Setup (1 minute)

```bash
# Clone/Navigate to project
cd Idea2Image

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

## Step 2: Install (1 minute)

```bash
pip install -r requirements.txt
```

## Step 3: Configure (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

## Step 4: Run (30 seconds)

```bash
python -m app.ui
```

Open browser to: **http://localhost:7860**

## Basic Usage

1. Enter your creative idea (e.g., "cyberpunk samurai")
2. Select scene attributes from dropdowns
3. Click "Generate Prompt"
4. Copy the refined prompt or download JSON package

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named openai` | Run `pip install -r requirements.txt` |
| Port 7860 in use | Use different port: `GRADIO_SERVER_PORT=8000 python -m app.ui` |
| Missing prompt bank | Ensure `data/sample_prompts.json` exists |
| API key error | Check `.env` file has valid `OPENAI_API_KEY` |

## Next Steps

- View full docs: See `Readme_new.md`
- Deployment: See `DEPLOYMENT.md`
- Contribute: See `CONTRIBUTING.md`
- Run tests: `pytest tests/ -v`
- Format code: `make format`

---
**Ready to go!** Questions? Check the README or open an issue.
