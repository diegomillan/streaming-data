FROM tiangolo/uvicorn-gunicorn-fastapi:latest

WORKDIR /src/app
COPY requirements.txt /tmp/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --requirement /tmp/requirements.txt
