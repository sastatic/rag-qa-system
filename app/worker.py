import json
import asyncio
from redis.asyncio import Redis
from services.document_processor import get_document_processor
from common import get_logger
from common.config import REDIS_HOST, REDIS_PORT


class DocumentWorker:
    def __init__(self):
        self.logger = get_logger("worker")
        self.redis_client = Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        self.document_processor = get_document_processor()
        self.channel = "document_processing"
        self.poll_interval = 0.1

    async def decode_message(self, message):
        try:
            data = json.loads(message.get("data", "{}"))
        except Exception as e:
            self.logger.exception("Failed to decode message: %s", e)
            return None
        document_id = data.get("document_id")
        if not document_id:
            self.logger.warning("Message missing document_id.")
            return None
        return document_id

    async def process_message(self, message):
        document_id = await self.decode_message(message)
        if not document_id:
            return
        self.logger.info("Received document id: %s for processing.", document_id)
        try:
            await self.document_processor.process_document(document_id)
        except Exception as e:
            self.logger.exception("Error processing document %s: %s", document_id, e)

    async def listen(self):
        await self.pubsub.subscribe(self.channel)
        self.logger.info("Subscribed to channel: %s", self.channel)
        while True:
            message = await self.pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message:
                await self.process_message(message)
            await asyncio.sleep(self.poll_interval)

    async def shutdown(self):
        await self.pubsub.close()
        await self.redis_client.close()

    async def run(self):
        try:
            await self.listen()
        except Exception as e:
            self.logger.exception("Worker encountered an error: %s", e)
        finally:
            await self.shutdown()


if __name__ == "__main__":
    worker = DocumentWorker()
    asyncio.run(worker.run())
