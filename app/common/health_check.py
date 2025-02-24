# app/health_check.py

import asyncio
import httpx
from redis.asyncio import Redis
from common import get_logger
from common.config import OLLAMA_HOST, REDIS_URL, OLLAMA_MODEL

logger = get_logger(__name__)

class ServiceHealthChecker:
    def __init__(self):
        self.redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
        self.OLLAMA_HOST = OLLAMA_HOST

    async def wait_for_redis(self):
        while True:
            try:
                if await self.redis_client.ping():
                    logger.info("Redis is ready.")
                    return
            except Exception:
                logger.info("Waiting for Redis to be ready...")
            await asyncio.sleep(1)

    async def wait_for_ollama(self):
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.OLLAMA_HOST}/api/tags")
                    if response.status_code == 200:
                        logger.info("Ollama is ready.")
                        return
            except Exception:
                logger.info("Waiting for Ollama to be ready...")
            await asyncio.sleep(1)


    async def pull_model(self, model_name: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.OLLAMA_HOST}/api/tags")
                response.raise_for_status()
                data = response.json()
                models = data.get("models", [])
                available_models = [model.get("name") for model in models]
                logger.info(f"Available models: {available_models}")
                if model_name in available_models:
                    logger.info(f"Model '{model_name}' is already loaded.")
                    return
            except Exception as e:
                logger.info("Could not verify model list; proceeding to pull model. Error: %s", e)

            payload = {"name": model_name}
            headers = {"Content-Type": "application/json"}
            
            while True:
                response = await client.post(f"{self.OLLAMA_HOST}/api/pull", json=payload, headers=headers)
                if response.status_code == 200 and '"status":"success"' in response.text:
                    logger.info(f"Model '{model_name}' pulled successfully.")
                    return
                else:
                    logger.info("Model pull in progress. Response: %s", response.text)
                await asyncio.sleep(1)

    async def perform_health_checks(self):
        await self.wait_for_redis()
        await self.wait_for_ollama()
        await self.pull_model(OLLAMA_MODEL)
