FROM python:alpine

WORKDIR /app

COPY requirements.txt requirements.txt
ADD  tfl_bus_monitor tfl_bus_monitor
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--workers", "1", "--threads", "5", "--log-level=debug","main:app"]
