FROM python:3.11-slim-bookworm

WORKDIR /app

COPY . .


RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "-m", "manage", "runserver", "0.0.0.0:8080" ]