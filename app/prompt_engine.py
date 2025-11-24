"""
Prompt Engine - Template building and LLM refinement for image prompts.

Responsible for:
- Converting structured scene specs into template prompts
- Calling OpenAI LLM for prompt refinement
- Generating complementary negative prompts
"""

import logging
from .utils import get_env

logger = logging.getLogger(__name__)

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
LLM_MODEL = get_env("LLM_MODEL", "gpt-4o-mini")

client = None
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set. LLM refinement will be disabled.")
else:
    try:
        try:
            # Try new API (openai >= 1.0)
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
        except ImportError:
            # Fall back to old API (openai < 1.0)
            import openai
            openai.api_key = OPENAI_API_KEY
            client = openai
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        client = None

BASE_TEMPLATE = (
    "A {style} {subject} {action} in {location}, "
    "shot as a {camera} at {lighting}, mood: {mood}. "
    "Color palette: {palette}. Detail level: {detail}."
)


def build_template(scene_spec: dict) -> str:
    """
    Build a template prompt from scene specification.

    Args:
        scene_spec: Dictionary containing scene attributes

    Returns:
        Formatted template string
    """
    return BASE_TEMPLATE.format(
        style=scene_spec.get("style", "photorealistic"),
        subject=scene_spec.get("subject", "subject"),
        action=scene_spec.get("action", ""),
        location=scene_spec.get("location", ""),
        camera=scene_spec.get("camera", "wide-angle"),
        lighting=scene_spec.get("lighting", "soft"),
        mood=scene_spec.get("mood", "calm"),
        palette=scene_spec.get("palette", "neutral"),
        detail=scene_spec.get("detail", "high")
    )


def llm_refine(prompt: str, temperature: float = 0.6,
               max_tokens: int = 200) -> tuple[str, str]:
    """
    Refine prompt using OpenAI LLM and generate negative prompt.

    Sends the draft prompt to GPT for expansion and refinement,
    then generates a complementary negative prompt.

    Args:
        prompt: Template prompt to refine
        temperature: LLM temperature (0.0-2.0), default 0.6
        max_tokens: Maximum tokens in response, default 200

    Returns:
        Tuple of (refined_prompt, negative_prompt)
    """
    if not client or not OPENAI_API_KEY:
        logger.warning("OpenAI client not configured, returning unrefined "
                       "prompt")
        return prompt, "lowres, blurry, watermark, distorted, bad anatomy"

    system_msg = (
        "You are an assistant that converts short scene specs into "
        "production-ready image-generation prompts. "
        "Keep concise but highly descriptive."
    )

    user_msg = (
        f"Draft prompt: {prompt}\n\n"
        "Task: Refine this into a high-quality prompt for an AI image "
        "model. Then generate a negative prompt on a new line starting "
        "with 'NEGATIVE:'."
    )

    try:
        # Handle both old and new OpenAI API versions
        try:
            # New API (openai >= 1.0)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            text = response.choices[0].message.content.strip()
        except AttributeError:
            # Old API (openai < 1.0)
            response = client.ChatCompletion.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            text = response.choices[0].message.content.strip()

        if "NEGATIVE:" in text:
            parts = text.split("NEGATIVE:")
            refined = parts[0].strip()
            negative = parts[1].strip()
        else:
            refined = text
            negative = "lowres, blurry, watermark, distorted, bad anatomy"

        logger.info("Successfully refined prompt with LLM")
        return refined, negative

    except Exception as e:
        logger.error(f"Error during LLM refinement: {e}")
        return prompt, "lowres, blurry, watermark, distorted, bad anatomy"
