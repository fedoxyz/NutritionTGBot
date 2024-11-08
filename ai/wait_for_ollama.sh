#!/bin/bash

# Wait until the ready file is created by the Ollama container
echo "Waiting for Ollama to be ready..."
while [ ! -f /tmp/ollama_ready.tmp ]; do
  sleep 2
done
echo "Ollama is ready. Starting the application..."

rm /tmp/ollama_ready.tmp
