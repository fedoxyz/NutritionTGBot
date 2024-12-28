#!/bin/bash

# Retrieve product classification Keras model
echo "🔴 Retrieve product classification Keras model..."
filename="model.keras"
fileid="1h2jnwzU3YmjoWMY7CzPBezXJkaLfIT6M"
filepath="./models/${filename}"

if [ ! -f "$filepath" ]; then
  curl -L -o "$filepath" "https://drive.google.com/uc?export=download&id=${fileid}"
  echo "🟢 Keras model downloaded."
else
  echo "🟢 Keras model already exists. Skipping download."
fi

# Retrieve product classification BERT model
echo "🔴 Retrieve product classification BERT model..."
filename="model.zip"
filepath="./models/${filename}"
extract_path="./models/bert"

echo "Current working directory:"
echo $(pwd)

# Check if BERT folder has contents
if [ ! "$(ls -A "$extract_path" 2>/dev/null)" ]; then
  echo "🔴 BERT folder is empty or does not exist. Downloading archive..."
  curl -L -o "$filepath" "https://drive.usercontent.google.com/download?id=1ZFQm356ga0umWPU_H8AOJCCBLOod4Uj3&export=download&confirm=t&uuid=258a8606-2666-4b54-95b0-77c4ffade3f3&at=APvzH3pPCqBVOVsCaPdvxCXYQA2_:1735351431985"
  echo "🔴 Unzipping BERT model archive..."
  mkdir -p "$extract_path"
  unzip -o "$filepath" -d "$extract_path"
  echo "🟢 BERT model extracted to $extract_path."
  rm "$filepath"
  echo "🟢 BERT archive removed."
else
  echo "🟢 BERT folder already has contents. Skipping download and extraction."
fi

# Wait for Ollama to be ready
echo "🔴 Waiting for Ollama to be ready..."
while [ ! -f /tmp/ollama_ready.tmp ]; do
  sleep 2
done
echo "🟢 Ollama is ready. Starting the application..."

# Clean up
rm /tmp/ollama_ready.tmp
