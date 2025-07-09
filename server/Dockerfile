FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        libpq-dev \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash app

WORKDIR /server
COPY . /server

RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

USER app

WORKDIR /

CMD ["/wait-for-db.sh", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]