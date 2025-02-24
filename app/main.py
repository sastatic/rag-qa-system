# app/main.py

from fastapi import FastAPI
from api import documents, qa
from common import get_logger
from common.health_check import ServiceHealthChecker
from contextlib import asynccontextmanager

logger = get_logger("main_server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    health_checker = ServiceHealthChecker()
    logger.info("Starting service health checks...")
    await health_checker.perform_health_checks()
    logger.info("All services are healthy. Starting application.")
    yield


app = FastAPI(title="RAG Q&A System", lifespan=lifespan)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(qa.router, prefix="/qa", tags=["qa"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Q&A System"}
