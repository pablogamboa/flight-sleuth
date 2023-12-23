FROM python:3.12.1

COPY app /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
