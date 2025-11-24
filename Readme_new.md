# Idea2Image — Turn Ideas into Rendering-Ready Prompts

A professional AI-ML application that transforms creative ideas into detailed, optimized prompts for AI image generation models. Combines structured templates, semantic search, and LLM refinement to produce production-ready image prompts.

## Features

- **Interactive Web UI** - Gradio-based interface for easy prompt composition
- **Structured Scene Building** - Dropdown-based scene attribute selection
- **LLM Refinement** - OpenAI GPT integration for prompt enhancement
- **Smart Suggestions** - Semantic search-based prompt bank suggestions using FAISS
- **JSON Export** - Downloadable packages with prompts, parameters, and metadata
- **Error Handling** - Graceful fallbacks and comprehensive logging
- **Production Ready** - Full type hints, docstrings, and proper project structure

## Architecture

```
Idea2Image/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── ui.py                    # Gradio web interface
│   ├── prompt_engine.py         # Template building & LLM refinement
│   ├── retrieval.py             # Semantic search with FAISS
│   ├── output_formatter.py      # JSON packaging
│   ├── utils.py                 # Environment & utility functions
│   ├── attribute_config.json    # Scene attributes configuration
│   └── __pycache__/             # Python cache (ignored)
├── data/
│   └── sample_prompts.json      # Curated prompt bank
├── tests/                       # Unit tests
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── Readme.md                    # Original file (legacy)
```

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (for LLM refinement)

### Installation

1. **Clone and Setup**
   ```bash
   cd Idea2Image
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_key_here
   LLM_MODEL=gpt-4o-mini
   ```

4. **Run Application**
   ```bash
   python -m app.ui
   ```
   The app will start at `http://localhost:7860`

## Usage

1. **Enter Your Idea** - Describe your creative concept (optional but recommended)

2. **Select Attributes** - Choose from dropdowns:
   - **Subject**: Type of subject (person, landscape, castle, etc.)
   - **Style**: Artistic style (photorealistic, illustration, etc.)
   - **Camera**: Camera perspective (wide-angle, telephoto, macro, etc.)
   - **Lighting**: Lighting setup (sunset, studio, neon, etc.)
   - **Mood**: Overall atmosphere (mysterious, joyful, epic, etc.)
   - **Palette**: Color palette (warm, cool, vibrant, etc.)

3. **Add Details** - Optional text fields:
   - **Action/Pose**: What the subject is doing
   - **Location/Setting**: Environmental context
   - **Detail Level**: Slider for detail intensity (1-10)

4. **Generate** - Click "Generate Prompt" button

5. **Results** - Get:
   - **Final Prompt**: Refined, ready-to-use prompt
   - **Negative Prompt**: Undesired attributes
   - **Suggestions**: Related prompts from prompt bank
   - **Scene Spec**: Your configuration as JSON
   - **Download Package**: Complete JSON file with metadata

## Dependencies

### Core
- **gradio** (≥3.0) - Web interface
- **openai** (≥1.0.0) - LLM API client
- **python-dotenv** - Environment variable management

### ML/Embeddings
- **sentence-transformers** - Semantic embeddings (all-MiniLM-L6-v2)
- **faiss-cpu** - Vector similarity search
- **numpy** - Numerical operations
- **pandas** - Data manipulation (optional)

See `requirements.txt` for exact versions.

## Configuration

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=sk-...

# Optional
LLM_MODEL=gpt-4o-mini          # GPT model to use
DEBUG=False                     # Enable debug logging
LOG_LEVEL=INFO                  # Logging level
```

### Attribute Configuration (app/attribute_config.json)

Customize available options:
```json
{
  "subjects": ["person", "landscape", "castle", "car", "product", "animal"],
  "styles": ["photorealistic", "illustration", "concept art", "watercolor"],
  "lighting": ["sunset", "noon", "studio", "cinematic", "neon"],
  "camera": ["wide-angle", "telephoto", "macro", "portrait", "aerial"],
  "moods": ["mysterious", "joyful", "melancholic", "epic", "calm"],
  "palettes": ["warm", "cool", "monochrome", "vibrant", "pastel"]
}
```

## Module Documentation

### app/ui.py
The main Gradio interface. Handles:
- UI component creation and layout
- Event handling and validation
- Error display and logging
- Attribute loading from config

### app/prompt_engine.py
Prompt generation engine:
- **build_template()** - Creates template from scene spec
- **llm_refine()** - Calls OpenAI to enhance prompt and generate negative prompt

### app/retrieval.py
Semantic search system:
- **PromptRetrieval** - FAISS-based retrieval from prompt bank
- Uses all-MiniLM-L6-v2 embeddings for semantic similarity

### app/output_formatter.py
Packages the final output:
- **package_output()** - Creates downloadable JSON with metadata

### app/utils.py
Utility functions:
- **get_env()** - Safe environment variable access

## Error Handling

The application includes robust error handling:

- **Missing OpenAI API Key** - Falls back to unrefined prompts with warning
- **Failed Retrieval** - Returns empty suggestions gracefully
- **LLM API Errors** - Uses fallback negative prompt
- **Missing Config/Data Files** - Uses sensible defaults
- **Invalid JSON** - Logs errors and continues

All errors are logged for debugging.

## Logging

Enable debug logging to troubleshoot:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Logs include:
- Config file loading status
- Retriever initialization
- LLM refinement attempts
- API errors and warnings

## Development

### Adding Custom Attributes

1. Edit `app/attribute_config.json`:
   ```json
   {
     "new_attribute": ["option1", "option2", "option3"]
   }
   ```

2. Update `app/ui.py` to add corresponding dropdown in UI

3. Update `app/prompt_engine.py` BASE_TEMPLATE if needed

### Running Tests

```bash
python -m pytest tests/ -v
```

### Code Style

Project follows PEP 8 with:
- Type hints for all functions
- Comprehensive docstrings
- 79-character line limit
- Logging for debugging

## Examples

### Example 1: Fantasy Character
```
Idea: A powerful wizard casting a spell
Subject: person
Style: illustration
Mood: epic
Camera: portrait
Lighting: studio
Palette: cool
Detail: 9
```

### Example 2: Sci-Fi Landscape
```
Idea: Alien planet with floating islands
Subject: landscape
Style: concept art
Mood: mysterious
Camera: aerial
Lighting: neon
Palette: vibrant
Detail: 10
```

## Troubleshooting

**Issue**: "OpenAI API key not found"
- **Solution**: Create `.env` file and add `OPENAI_API_KEY`

**Issue**: "Failed to load embedding model"
- **Solution**: Ensure `sentence-transformers` and `torch` are installed
  ```bash
  pip install sentence-transformers torch
  ```

**Issue**: "Prompt bank not found"
- **Solution**: Ensure `data/sample_prompts.json` exists in project root

**Issue**: Web interface not loading
- **Solution**: Check Gradio installation and port availability (default 7860)

## Performance Notes

- **First run**: Model downloads (~150MB for embeddings)
- **Inference time**: 
  - Template building: <1ms
  - Semantic search: 10-50ms
  - LLM refinement: 1-5 seconds (depends on API)
  - Total: 2-10 seconds per prompt

- **Memory usage**: ~500MB (including model cache)

## Future Enhancements

- [ ] Multiple LLM provider support (Claude, Anthropic, local)
- [ ] Batch prompt generation
- [ ] User prompt bank management
- [ ] Prompt history/versioning
- [ ] API endpoint for programmatic access
- [ ] Web deployment configuration
- [ ] Advanced filtering and weighting
- [ ] Prompt statistics and analytics

## License

[Add your license here]

## Contributing

[Add contribution guidelines]

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review debug logs (`LOG_LEVEL=DEBUG`)
3. Open an issue with:
   - Error message/screenshot
   - Steps to reproduce
   - Environment details (Python version, OS)

---

**Last Updated**: November 2025
**Version**: 0.1.0
**Status**: Production Ready ✓
