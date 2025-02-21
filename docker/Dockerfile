# Builder Stage: Install build dependencies and install the project
FROM python:3.13-slim AS builder

# Install system build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

WORKDIR /app

# Copy dependency configuration and application code
COPY app/pyproject.toml .
COPY app/ app/

# Upgrade pip and install the project (which reads pyproject.toml)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir .

# Production Stage: Create a lean runtime image
FROM python:3.13-slim

WORKDIR /app

# Copy installed packages and binaries from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code (for any runtime assets)
COPY --from=builder /app/app /app

# Expose the port that the application will run on
EXPOSE 8000

# Set the ENTRYPOINT to run your FastAPI app with uvicorn
ENTRYPOINT ["uvicorn", "main:app"]