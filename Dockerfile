# Stage 1: Build
FROM python:3.9-slim as builder

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /usr/src/app
COPY --from=builder /root/.local /root/.local
COPY app ./app

ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000

CMD ["python", "./app/main.py"]
