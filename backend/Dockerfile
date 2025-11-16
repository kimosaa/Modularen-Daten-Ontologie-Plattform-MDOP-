# Multi-stage build for MDOP Backend
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# ========== Development Stage ==========
FROM base as development

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ========== Production Stage ==========
FROM base as production

# Copy requirements
COPY requirements.txt .

# Install only production dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y pytest pytest-asyncio pytest-cov

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 mdop && \
    chown -R mdop:mdop /app

USER mdop

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application with gunicorn for production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
