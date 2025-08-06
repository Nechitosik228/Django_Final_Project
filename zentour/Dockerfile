FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt update && \
    apt install -y gcc libpq-dev build-essential postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "uvicorn zentour.asgi:application --host 0.0.0.0 --port $PORT"]