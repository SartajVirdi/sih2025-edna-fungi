FROM python:3.10-slim
RUN apt-get update && apt-get install -y build-essential wget ca-certificates git \
    && apt-get install -y default-jre-headless libbz2-dev zlib1g-dev liblzma-dev \
    && apt-get install -y net-tools procps \
    && apt-get clean
# Install blast+
RUN apt-get update && apt-get install -y ncbi-blast+ seqtk && apt-get clean

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENTRYPOINT ["/bin/bash"]
