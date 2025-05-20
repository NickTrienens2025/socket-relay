FROM python:3.11-slim

WORKDIR /app

COPY relay.py .

RUN pip install websockets

CMD ["python", "relay.py"]