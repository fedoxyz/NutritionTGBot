FROM python:3.10-slim

COPY ./ai/requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc libgl1 libglib2.0-0 libpython3-dev && \
        rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051

# Add a script to wait for Ollama readiness
COPY ./ai/wait_for_ollama.sh /wait_for_ollama.sh
RUN chmod +x /wait_for_ollama.sh

ENV PYTHONPATH=/

# Start the application after waiting
CMD ["/bin/bash", "-c", "sh ./wait_for_ollama.sh && python grpc_server.py"]
