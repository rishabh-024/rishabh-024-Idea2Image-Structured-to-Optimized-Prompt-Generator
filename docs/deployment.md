# Deployment

This document explains how to deploy Idea2Image in development and production settings.

Local Docker (development)

1. Build the Docker image:

```powershell
.\dev.ps1 -Task docker-build
```

2. Run the container (pass `OPENAI_API_KEY` as env var):

```powershell
docker run -p 7860:7860 -e OPENAI_API_KEY=$env:OPENAI_API_KEY idea2image:latest
```

Docker Compose
- `docker-compose.yml` is included for multi-container setups. Use `docker-compose up --build` to start.

Production considerations
- Secrets: store `OPENAI_API_KEY` in a secure secrets manager or environment variables at runtime — do not commit secrets to the repo.
- Scalability: the current app runs a single Gradio process. For production, consider:
  - A reverse proxy (nginx) in front of the Gradio app
  - Serving the model backend separately if doing heavy embedding/model computation
  - Using an external vector DB (Pinecone, Milvus, Weaviate) instead of local FAISS for large-scale retrieval

Load balancing & autoscaling
- Put the app behind a load balancer and use multiple replicas for traffic. Persisted state (e.g., a serialized FAISS index or vector DB) is needed to ensure each replica can serve retrieval queries.

Monitoring
- Add application metrics (Prometheus/OpenTelemetry) and logging to track latency and error rates.
