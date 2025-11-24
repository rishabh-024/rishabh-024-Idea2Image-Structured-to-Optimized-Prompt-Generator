"""Unit tests for Idea2Image project."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


# Tests for prompt_engine.py
class TestPromptEngine:
    """Test cases for prompt template building and LLM refinement."""

    def test_build_template_basic(self):
        """Test basic template building with required fields."""
        from app.prompt_engine import build_template

        scene_spec = {
            "subject": "knight",
            "style": "photorealistic",
            "camera": "portrait",
            "lighting": "dramatic",
            "mood": "heroic",
            "palette": "warm",
            "action": "standing",
            "detail": "high",
            "location": "castle"
        }

        result = build_template(scene_spec)

        assert "knight" in result
        assert "photorealistic" in result
        assert "portrait" in result
        assert "dramatic" in result
        assert "heroic" in result
        assert "warm" in result

    def test_build_template_defaults(self):
        """Test that missing fields are handled with defaults."""
        from app.prompt_engine import build_template

        scene_spec = {}
        result = build_template(scene_spec)

        # Should use all defaults
        assert "subject" in result or "high" in result
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_template_partial(self):
        """Test template with some fields missing."""
        from app.prompt_engine import build_template

        scene_spec = {
            "subject": "dragon",
            "style": "digital art"
        }

        result = build_template(scene_spec)

        assert "dragon" in result
        assert "digital art" in result

    @patch('app.prompt_engine.client')
    def test_llm_refine_no_api_key(self, mock_client):
        """Test LLM refinement gracefully handles missing API key."""
        from app.prompt_engine import llm_refine

        with patch('app.prompt_engine.OPENAI_API_KEY', None):
            result_prompt, result_negative = llm_refine("test prompt")

            assert result_prompt == "test prompt"
            assert "lowres" in result_negative or "blurry" in result_negative

    def test_llm_refine_disabled(self):
        """Test that LLM refinement works when client is None."""
        from app.prompt_engine import llm_refine

        # Mock client as None
        with patch('app.prompt_engine.client', None):
            prompt, negative = llm_refine("A test prompt")

            assert prompt == "A test prompt"
            assert "blurry" in negative


# Tests for retrieval.py
class TestPromptRetrieval:
    """Test cases for semantic retrieval system."""

    def test_retrieval_initialization(self):
        """Test that retrieval system initializes."""
        from app.retrieval import PromptRetrieval

        # Use non-existent path for testing
        retriever = PromptRetrieval(bank_path="/nonexistent/path.json")

        assert retriever is not None
        assert retriever.prompts == []

    def test_retrieval_empty_index(self):
        """Test retrieval on empty index."""
        from app.retrieval import PromptRetrieval

        retriever = PromptRetrieval(bank_path="/nonexistent/path.json")
        results = retriever.retrieve("test query", k=3)

        assert results == []

    def test_retrieval_with_sample_data(self):
        """Test retrieval with sample prompt bank."""
        from app.retrieval import PromptRetrieval

        # Use actual sample_prompts.json if it exists
        bank_path = (Path(__file__).parent.parent / "data" / "sample_prompts.json")

        if bank_path.exists():
            retriever = PromptRetrieval(bank_path=str(bank_path))

            if retriever.index is not None:
                results = retriever.retrieve("neon alley", k=2)
                assert isinstance(results, list)


# Tests for output_formatter.py
class TestOutputFormatter:
    """Test cases for output packaging."""

    def test_package_output_structure(self):
        """Test that output package has correct structure."""
        from app.output_formatter import package_output

        prompt = "A beautiful landscape"
        negative = "blurry, low quality"
        params = {"sampler": "ddim", "steps": 30}

        result = package_output(prompt, negative, params)

        # Should be valid JSON
        data = json.loads(result)

        assert data["prompt"] == prompt
        assert data["negative_prompt"] == negative
        assert data["params"]["sampler"] == "ddim"
        assert "generated_at" in data

    def test_package_output_timestamp(self):
        """Test that package includes timestamp."""
        from app.output_formatter import package_output

        result = package_output("test", "test_neg", {})
        data = json.loads(result)

        assert "generated_at" in data
        assert "Z" in data["generated_at"]  # ISO format with Z

    def test_package_output_empty_params(self):
        """Test packaging with empty parameters."""
        from app.output_formatter import package_output

        result = package_output("prompt", "neg", {})
        data = json.loads(result)

        assert data["params"] == {}


# Tests for utils.py
class TestUtils:
    """Test cases for utility functions."""

    def test_get_env_existing(self):
        """Test getting existing environment variable."""
        from app.utils import get_env

        with patch.dict('os.environ', {'TEST_VAR': 'test_value'}):
            result = get_env('TEST_VAR')
            assert result == 'test_value'

    def test_get_env_missing_with_default(self):
        """Test getting missing variable returns default."""
        from app.utils import get_env

        with patch.dict('os.environ', {}, clear=True):
            result = get_env('NONEXISTENT', 'default_value')
            assert result == 'default_value'

    def test_get_env_missing_no_default(self):
        """Test getting missing variable without default."""
        from app.utils import get_env

        with patch.dict('os.environ', {}, clear=True):
            result = get_env('NONEXISTENT')
            assert result is None


# Integration tests
class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_prompt_generation_flow(self):
        """Test complete flow from spec to output."""
        from app.prompt_engine import build_template
        from app.output_formatter import package_output

        # Create scene spec
        scene_spec = {
            "subject": "warrior",
            "style": "digital art",
            "camera": "wide-angle",
            "lighting": "sunset",
            "mood": "heroic",
            "palette": "warm",
            "action": "running",
            "detail": "high",
            "location": "battlefield"
        }

        # Build template
        prompt = build_template(scene_spec)
        assert len(prompt) > 0

        # Package output
        params = {"steps": 30, "cfg_scale": 7.0}
        output = package_output(prompt, "blurry", params)

        # Verify JSON structure
        data = json.loads(output)
        assert "prompt" in data
        assert "negative_prompt" in data
        assert "params" in data

    def test_scene_spec_validation(self):
        """Test that scene spec handles various inputs."""
        from app.prompt_engine import build_template

        specs = [
            {"subject": "person"},
            {"style": "photorealistic"},
            {},
            {"subject": "", "style": ""},
        ]

        for spec in specs:
            result = build_template(spec)
            assert isinstance(result, str)
            assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
