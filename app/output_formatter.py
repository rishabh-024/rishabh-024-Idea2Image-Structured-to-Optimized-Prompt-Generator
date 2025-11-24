"""
Output Formatter - Package final prompts for download.

Combines refined prompt, negative prompt, and generation parameters
into a single downloadable JSON package.
"""

import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def package_output(prompt: str, negative: str,
                   params: dict) -> str:
    """
    Package prompt data into downloadable JSON format.

    Combines the refined positive and negative prompts with
    generation parameters and metadata into a structured JSON.

    Args:
        prompt: Refined positive prompt
        negative: Negative prompt
        params: Dictionary of generation parameters

    Returns:
        JSON-formatted string of packaged output
    """
    package = {
        "prompt": prompt,
        "negative_prompt": negative,
        "params": params,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    logger.debug("Packaged output successfully")
    return json.dumps(package, indent=2)
