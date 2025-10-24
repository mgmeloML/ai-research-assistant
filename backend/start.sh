#!/bin/bash
# Start Ollama in the background
ollama serve &

# Wait a few seconds for Ollama to initialize
sleep 5

# Load needed models
ollama pull nomic-embed-text
ollama pull granite3.3:8b

# Start FastAPI (via uvicorn)
exec uvicorn main:app --host 0.0.0.0 --port 8000
