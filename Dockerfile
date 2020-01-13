FROM python:3.8.1-alpine

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app/
COPY requirements.txt /app

RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN pip install -r requirements.txt

COPY /app /app

COPY .flake8 /app

