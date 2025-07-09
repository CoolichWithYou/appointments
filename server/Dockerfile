FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash app

WORKDIR /server
COPY . /server

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

USER app

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

WORKDIR /

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
