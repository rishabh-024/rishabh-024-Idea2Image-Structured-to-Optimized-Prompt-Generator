"""
Gradio UI for Idea2Image - Interactive prompt generation interface.

Provides a web interface for users to compose scene specifications and
generate refined AI image prompts with suggestions from a prompt bank.
"""

import logging
import json as _json
from pathlib import Path
from typing import Tuple

import gradio as gr

from .prompt_engine import build_template, llm_refine
from .retrieval import PromptRetrieval
from .output_formatter import package_output

# Setup logging
logger = logging.getLogger(__name__)

# Load attribute configuration
ATTR_PATH = Path(__file__).parent / "attribute_config.json"
try:
    with open(ATTR_PATH, "r", encoding="utf-8") as f:
        ATTR = _json.load(f)
    logger.info(f"Loaded attribute config from {ATTR_PATH}")
except Exception as e:
    logger.error(f"Failed to load attribute config: {e}")
    ATTR = {
        "subjects": ["person"],
        "styles": ["photorealistic"],
        "lighting": ["cinematic"],
        "camera": ["wide-angle"],
        "moods": ["mysterious"],
        "palettes": ["vibrant"]
    }

# Initialize retriever with error handling
PROMPTS_PATH = Path(__file__).parent.parent / "data" / "sample_prompts.json"
try:
    retriever = PromptRetrieval(bank_path=str(PROMPTS_PATH))
    logger.info(f"Initialized PromptRetrieval with {len(retriever.prompts)} "
                "prompts")
except Exception as e:
    logger.error(f"Failed to initialize retriever: {e}")
    retriever = None


def generate(scene_idea: str, subject: str, style: str, camera: str,
             lighting: str, mood: str, palette: str, action: str,
             detail: float, location: str) -> Tuple[
                 str, str, str, str, str]:
    """
    Generate refined prompt from scene specification.

    Args:
        scene_idea: User's creative idea description
        subject: Type of subject to render
        style: Artistic style
        camera: Camera perspective/type
        lighting: Lighting setup
        mood: Overall mood/atmosphere
        palette: Color palette
        action: Action or pose of subject
        detail: Detail level (1-10)
        location: Scene location/setting

    Returns:
        Tuple of (refined_prompt, negative_prompt, suggestions,
                  scene_spec_json, output_package_json)
    """
    try:
        # Build scene specification
        scene_spec = {
            "subject": subject or "subject",
            "style": style or "photorealistic",
            "camera": camera or "wide-angle",
            "lighting": lighting or "soft",
            "mood": mood or "calm",
            "palette": palette or "neutral",
            "action": action or "",
            "detail": detail or "high",
            "location": location or ""
        }

        # Build template from spec
        draft = build_template(scene_spec)
        logger.debug(f"Generated draft prompt: {draft[:50]}...")

        # Get retrieval suggestions
        suggestion_text = ""
        if retriever is not None:
            try:
                suggestions = retriever.retrieve(scene_idea or draft, k=3)
                suggestion_text = "\n".join(
                    [s.get("prompt", "") for s in suggestions]
                )
                logger.debug(f"Retrieved {len(suggestions)} suggestions")
            except Exception as e:
                logger.warning(f"Failed to retrieve suggestions: {e}")
                suggestion_text = "Unable to retrieve suggestions"

        # Refine with LLM
        try:
            refined, negative = llm_refine(draft)
            logger.info("Successfully refined prompt with LLM")
        except Exception as e:
            logger.error(f"LLM refinement failed: {e}")
            refined = draft
            negative = "lowres, blurry, watermark, distorted, bad anatomy"

        # Package output
        params = {
            "sampler": "ddim",
            "cfg_scale": 7.0,
            "steps": 30,
            "aspect_ratio": "16:9"
        }
        package = package_output(refined, negative, params)

        return (refined, negative, suggestion_text,
                _json.dumps(scene_spec, indent=2), package)

    except Exception as e:
        logger.exception("Error in generate function")
        error_msg = f"Error generating prompt: {str(e)}"
        return ("", "", error_msg, "{}", "{}")


# Build Gradio interface
with gr.Blocks(
    title="Idea2Image — Scene Composer",
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown(
        "# Idea2Image — Turn ideas into rendering-ready prompts\n\n"
        "Create detailed AI image prompts by specifying scene attributes. "
        "Get refinements and suggestions automatically."
    )

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("## Scene Configuration")

            idea = gr.Textbox(
                label="Your idea (one line)",
                placeholder=(
                    "e.g. lonely cyberpunk samurai in neon alley"
                ),
                lines=2
            )

            subject = gr.Dropdown(
                label="Subject",
                choices=ATTR.get("subjects", ["person"]),
                value="person"
            )

            style = gr.Dropdown(
                label="Style",
                choices=ATTR.get("styles", ["photorealistic"]),
                value="photorealistic"
            )

            camera = gr.Dropdown(
                label="Camera",
                choices=ATTR.get("camera", ["wide-angle"]),
                value="wide-angle"
            )

            lighting = gr.Dropdown(
                label="Lighting",
                choices=ATTR.get("lighting", ["cinematic"]),
                value="cinematic"
            )

            mood = gr.Dropdown(
                label="Mood",
                choices=ATTR.get("moods", ["mysterious"]),
                value="mysterious"
            )

            palette = gr.Dropdown(
                label="Palette",
                choices=ATTR.get("palettes", ["vibrant"]),
                value="vibrant"
            )

            action = gr.Textbox(
                label="Action / Pose",
                placeholder="e.g. standing, running",
                lines=1
            )

            detail = gr.Slider(
                label="Detail level",
                minimum=1,
                maximum=10,
                value=8,
                step=1
            )

            location = gr.Textbox(
                label="Location/Setting",
                placeholder="e.g. neon-lit alley",
                lines=1
            )

            generate_btn = gr.Button(
                "Generate Prompt",
                variant="primary",
                scale=2
            )

        with gr.Column(scale=3):
            gr.Markdown("## Results")

            out_prompt = gr.Textbox(
                label="Final Prompt",
                lines=6,
                interactive=False
            )

            out_negative = gr.Textbox(
                label="Negative Prompt",
                lines=2,
                interactive=False
            )

            out_suggestions = gr.Textbox(
                label="Suggestions from prompt bank",
                lines=4,
                interactive=False
            )

            out_spec = gr.JSON(label="Scene Spec (JSON)")

            out_package = gr.Textbox(
                label="Download Package (JSON)",
                lines=8,
                interactive=False
            )

    # Connect button to generate function
    generate_btn.click(
        generate,
        inputs=[
            idea, subject, style, camera, lighting, mood, palette,
            action, detail, location
        ],
        outputs=[
            out_prompt, out_negative, out_suggestions, out_spec, out_package
        ]
    )

    # Add examples
    gr.Examples(
        examples=[
            [
                "A warrior in a mystical forest",
                "person",
                "illustration",
                "wide-angle",
                "sunset",
                "epic",
                "warm",
                "wielding a sword",
                8,
                "enchanted forest"
            ],
            [
                "Futuristic city skyline",
                "landscape",
                "photorealistic",
                "telephoto",
                "neon",
                "mysterious",
                "cool",
                "",
                9,
                "cyberpunk metropolis"
            ]
        ],
        inputs=[
            idea, subject, style, camera, lighting, mood, palette,
            action, detail, location
        ]
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo.launch(server_name="0.0.0.0", share=False)
