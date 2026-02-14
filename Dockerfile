FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Default env vars (overridden by Render environment variables)
ENV ALLOWED_ORIGINS=*
ENV DEBUG=False

# Render uses PORT env var (default 10000)
ENV PORT=10000
EXPOSE ${PORT}

# Start server - admin user is created in FastAPI lifespan
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
