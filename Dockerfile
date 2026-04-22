# builder
FROM python:3.12-slim AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
