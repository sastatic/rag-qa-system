# Use Python 3.13-slim for development
FROM python:3.13-slim

WORKDIR /app

# Install system build tools and curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency configuration and install the project
COPY app/pyproject.toml .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir .

# Expose the port your app will run on
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
