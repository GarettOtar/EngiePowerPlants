# syntax=docker/dockerfile:1
FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /EngiePowerplants
COPY requirements.txt /EngiePowerplants/
RUN pip install -r requirements.txt
COPY . /EngiePowerplants
