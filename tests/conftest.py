"""Test configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_scene_spec():
    """Fixture providing sample scene specification."""
    return {
        "subject": "person",
        "style": "photorealistic",
        "camera": "portrait",
        "lighting": "studio",
        "mood": "serious",
        "palette": "neutral",
        "action": "posing",
        "detail": "high",
        "location": "studio"
    }


@pytest.fixture
def sample_params():
    """Fixture providing sample generation parameters."""
    return {
        "sampler": "ddim",
        "cfg_scale": 7.0,
        "steps": 30,
        "aspect_ratio": "16:9"
    }


@pytest.fixture
def sample_prompts():
    """Fixture providing sample prompts."""
    return [
        "neon-lit alley, wet pavement, volumetric fog",
        "heroic portrait, rim light, shallow depth of field",
        "low poly stylized landscape, pastel palette"
    ]
