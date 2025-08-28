FROM python:3.10-slim AS builder

WORKDIR /app

# System dependencies needed for numpy, pandas, faiss, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        wget \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install optimized dependencies (CPU-only torch, no cache)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt

# Final stage: smaller runtime image
FROM python:3.10-slim

WORKDIR /app

# Copy installed python packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY advisor_service /

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

EXPOSE 5000

CMD ["python", "run.py"]
