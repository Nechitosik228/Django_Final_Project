FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev build-essential postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]