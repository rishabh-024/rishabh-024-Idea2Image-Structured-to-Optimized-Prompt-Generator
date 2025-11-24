# Usage

This document explains how to use the running application and the UI features.

Access the UI
- When running with `.\dev.ps1 -Task run`, open `http://localhost:7860` in your browser.

UI Walkthrough
- Left column includes inputs for scene attributes. Typical fields: `subject`, `style`, `lighting`, `camera`, `mood`, `palette`, and additional sliders for detail/seed.
- Right column shows generated prompt and examples from the embedded prompt bank.
- Buttons: `Generate` builds a prompt (locally) and optionally refines it via the LLM. `Export` downloads a JSON package containing the prompt and metadata created by `app/output_formatter.py`.

LLM Refinement
- The prompt engine has a configurable option to call an LLM to refine or rephrase the base prompt. If the OpenAI API key is not configured, the system will return the base template only.

Using the Windows helper (`dev.ps1`)
- Install dev dependencies: `.\dev.ps1 -Task dev-install`
- Run app: `.\dev.ps1 -Task run`
- Run tests: `.\dev.ps1 -Task test`

Exported artifacts
- JSON artifact fields: `prompt`, `negative_prompt`, `params`, `generated_at`.
- The output is suitable for copy/paste into image generation frontends (Stable Diffusion, Midjourney-style prompts, or API inputs).
