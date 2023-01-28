FROM python:3.10-slim as build

ADD ./requirements.txt .

RUN apt-get update && apt-get upgrade -y && \
    apt-get install gcc -y &&  \
    pip install -r requirements.txt

ADD ./app ./app


ENTRYPOINT ["/bin/sh", "-c", "gunicorn 'app.main:app' -b 0.0.0.0:8000"]

EXPOSE 8000
