FROM python:4.2

LABEL maintainer="hameddjf"

ENV PYTHONUNBUFFERED 1

COPY .\requirements.txt .\tmp\requirements.txt

copy .\requirements.dev.txt .\tmp\requirements.dev.txt

copy .\app \app

WORKDIR ./app

RUN pip install --upgrade pip && \
    pip install requirements.txt && \
    pip install requirements.dev.txt && \