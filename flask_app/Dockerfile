FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--workers", "1", "--threads", "5", "main:app"]
