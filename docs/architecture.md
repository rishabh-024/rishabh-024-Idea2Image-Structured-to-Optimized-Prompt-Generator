# Architecture

This document explains the high-level architecture of the Idea2Image project and details of the main components.

Overview
- Purpose: convert a short idea/scene description into an optimized prompt for image-generation models.
- High-level flow:
  1. UI accepts structured scene attributes from the user (subject, style, lighting, camera, mood, palette, etc.).
  2. Retrieval module searches a local prompt bank and returns semantically-similar prompts as inspiration.
  3. Prompt engine composes a base template from attributes and optionally calls an LLM (OpenAI) to refine the prompt.
  4. Output formatter packages the final prompt, negative prompt, and parameters into a JSON artifact for export.

Main Components

- `app/ui.py`
  - Gradio Blocks-based interactive interface.
  - Inputs: scene attribute selectors, free-text overrides, numeric parameters.
  - Orchestrates calls to `prompt_engine`, `retrieval`, and `output_formatter`.

- `app/prompt_engine.py`
  - Builds a human-readable template from the selected attributes.
  - Handles LLM refinement using OpenAI SDK with backward/forward compatibility logic (supports older and newer OpenAI Python SDK variants).
  - Contains defensive error handling and timeouts to avoid blocking the UI.

- `app/retrieval.py`
  - Loads a prompt bank (`data/sample_prompts.json`) and computes/loads embeddings (Sentence Transformers).
  - Builds and queries a FAISS index for semantic similarity.
  - Returns top-k candidate prompts with scores and metadata.

- `app/output_formatter.py`
  - Packages prompt, negative prompt, and generation parameters into a well-formed JSON object with metadata such as `generated_at`.

- `app/utils.py`
  - Environment helpers and small utility functions (e.g., `get_env()` to read `.env`).

Data & Models
- `data/sample_prompts.json` — sample prompt bank used for retrieval during development.
- `app/attribute_config.json` — configuration for UI dropdowns (subjects, styles, moods, palettes).
- Dependencies:
  - Sentence Transformers (embedding model: all-MiniLM-L6-v2 or configured model)
  - FAISS (for approximate nearest neighbor search)
  - OpenAI Python SDK (compatible with versions >=0.28 and 1.x/2.x via compatibility layer)

Security and secrets
- API keys (OpenAI) are loaded from environment or `.env`. Do not commit `.env` with secrets.

Extensibility
- The architecture separates concerns: retrieval, prompt composition, LLM refinement, and UI orchestration. You can replace any component (e.g., use a different vector DB or an alternate LLM provider) with minimal changes.
