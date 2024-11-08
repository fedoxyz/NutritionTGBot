#!/bin/bash

# Wait until the ready file is created by the Ollama container
echo "Waiting for Ollama to be ready..."
while [ ! -f /tmp/ollama_ready ]; do
  sleep 2
done
echo "Ollama is ready. Starting the application..."
