import os
import asyncpg
from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["endpoint"])

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/appdb")

@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(DB_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

@app.get("/health")
async def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    async with app.state.pool.acquire() as conn:
        await conn.fetchval("SELECT 1")
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    REQUEST_COUNT.labels(endpoint="/metrics").inc()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
