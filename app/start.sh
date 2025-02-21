# app/start.sh

#!/bin/bash

# Get variables from environment
OLLAMA_HOST="${OLLAMA_HOST:-http://ollama:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-llama2}"

# Wait for Ollama to be ready
until curl -s "${OLLAMA_HOST}/api/tags" > /dev/null; do
    echo "Waiting for Ollama..."
    sleep 1
done

# Pull the model with proper waiting
echo "Pulling model: ${OLLAMA_MODEL}"
curl -s "${OLLAMA_HOST}/api/pull" -H 'Content-Type: application/json' \
    -d "{\"name\": \"${OLLAMA_MODEL}\"}" | while read -r line; do
    echo "$line"
    if echo "$line" | grep -q '"status":"success"'; then
        break
    fi
done

# Start the application
exec uvicorn main:app "$@"