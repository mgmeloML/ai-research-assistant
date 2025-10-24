# ------------------------
# Stage 1: Base Python environment
# ------------------------
FROM python:3.10-slim

# Set up working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code
COPY . .

# Expose FastAPI (8000) and Ollama (11434)
EXPOSE 8000 11434

# Copy and configure startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run startup script (runs Ollama + FastAPI)
CMD ["/start.sh"]
