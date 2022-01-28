#FROM python:3.9-slim
FROM arm32v7/python:3.9-slim

WORKDIR /opt/app

ARG CFLAGS=-Qunused-arguments
ARG CPPFLAGS=-Qunused-arguments

COPY . .

RUN apt update && apt -y install gcc
RUN pip install --no-cache-dir --default-timeout=100 -r requirements/prod.txt

ENTRYPOINT [ "./docker/entrypoint.sh" ]
