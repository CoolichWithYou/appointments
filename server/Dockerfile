FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["daphne", "main:app", "-b", "0.0.0.0"]
