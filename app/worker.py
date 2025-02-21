# app/worker.py

import json
import asyncio
from redis.asyncio import Redis
from services.document_processor import get_document_processor
from common import get_logger

redis_client = Redis(host='redis', port=6379, db=0, decode_responses=True)
document_processor = get_document_processor()
logger = get_logger('worker')

async def process_message(message):
    try:
        data = json.loads(message["data"])
        document_id = data.get("document_id")
        if document_id:
            logger.info(f"Received document id: {document_id} for processing.")
            await document_processor.process_document(document_id)
    except Exception as e:
        logger.exception(f"Error processing message: {e}")

async def main():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("document_processing")
    logger.info("Worker listening for document processing messages...")

    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if message:
            await process_message(message)
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(main())
