FROM python:3.10-slim

COPY ./requirements.txt requirements.txt

RUN apt update && \
    apt install --no-install-recommends -y gcc libgl1 libglib2.0-0 libpython3-dev gnupg && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

#CMD ["bash", "-c", "sleep infinity"]
CMD ["bash", "-c", "python3 bot.py"]
