FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04

# Set CUDA environment variables
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

COPY ./ai/requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc libgl1 libglib2.0-0 libpython3-dev libssl-dev libffi-dev python3-dev curl wget unzip&& \
        rm -rf /var/lib/apt/lists/* && \
    apt install -y python3.10 && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    ln -sf /usr/bin/python3.10 /usr/bin/python && \
    python get-pip.py && \
    ln -s /usr/local/bin/pip3.10 /usr/bin/pip

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051

COPY ./ai/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/

# Start the application after waiting
CMD ["/bin/bash", "-c", "sh ./entrypoint.sh && python grpc_server.py"]
