# Deployment Guide

## Local Development

```bash
python -m app.ui
```

Access at: http://localhost:7860

## Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

EXPOSE 7860

CMD ["python", "-m", "app.ui"]
```

Build and run:

```bash
docker build -t idea2image .
docker run -p 7860:7860 -e OPENAI_API_KEY=your_key_here idea2image
```

## Deployment on Hugging Face Spaces

1. Create new Space on Hugging Face
2. Connect GitHub repository
3. Add secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
4. Create `space_requirements.txt`:

```
gradio>=3.0
openai>=1.0.0
python-dotenv>=0.19.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
torch>=1.9.0
numpy>=1.21.0
pandas>=1.3.0
```

5. Create `app.py` in root:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.ui import demo

if __name__ == "__main__":
    demo.launch()
```

## Environment Variables

**Required:**
- `OPENAI_API_KEY` - Your OpenAI API key

**Optional:**
- `LLM_MODEL` - GPT model (default: gpt-4o-mini)
- `DEBUG` - Enable debug logging (default: False)
- `LOG_LEVEL` - Logging level (default: INFO)
- `GRADIO_SERVER_NAME` - Server address (default: 127.0.0.1)
- `GRADIO_SERVER_PORT` - Server port (default: 7860)

## Performance Optimization

1. **Model Caching**: First run downloads ~150MB
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; \
   SentenceTransformer('all-MiniLM-L6-v2')"
   ```

2. **Batch Processing**: Consider implementing batch mode for large-scale usage

3. **API Rate Limiting**: Monitor OpenAI usage

## Monitoring

Enable debug logging:

```bash
LOG_LEVEL=DEBUG python -m app.ui
```

Check logs for:
- Model loading times
- API call durations
- Error rates

## Troubleshooting Deployment

**Issue**: Port already in use
```bash
# Use different port
GRADIO_SERVER_PORT=8000 python -m app.ui
```

**Issue**: Out of memory
```bash
# Use GPU if available
# Reduce embedding batch size in retrieval.py
```

**Issue**: Slow API responses
```bash
# Check OpenAI rate limits
# Implement request caching
# Use async calls
```

## Production Checklist

- [ ] OPENAI_API_KEY configured securely
- [ ] Error logging enabled
- [ ] Rate limiting implemented
- [ ] Monitoring/alerts set up
- [ ] Database for history (optional)
- [ ] API authentication (if exposed)
- [ ] HTTPS enabled (reverse proxy)
- [ ] Backup strategy
- [ ] Performance tested
- [ ] Documentation updated
