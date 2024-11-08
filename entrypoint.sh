#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve LLAMA3.2-vision model..."
ollama pull llama3.2-vision
echo "🟢 Done!"

echo "🔴 Retrieve LLAMA3.2 model..."
ollama pull llama3.2
echo "🟢 Done!"

# Create a ready file to indicate that models have been pulled
touch /tmp/ollama_ready.tmp

# Wait for Ollama process to finish
wait $pid
