# Dockerfile for RAG System
# Build: docker build -t rag-system .
# Run: docker run -p 5000:5000 -v /path/to/data:/app/data rag-system

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p outputs data

# Expose port
EXPOSE 5000

# Default command
CMD ["python", "main.py", "--csv", "/app/data/conversations.csv", "--host", "0.0.0.0", "--port", "5000"]
