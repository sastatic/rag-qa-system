# app/services/document_service.py
import os
import shutil
from fastapi import HTTPException
from database import create_s3_client
from repositories.document_repository import DocumentRepository
from common import get_logger
from ulid import ULID
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from common.config import REDIS_HOST, REDIS_PORT, BUCKET_RAGQA
import json

logger = get_logger(__name__)
s3_client = create_s3_client()

class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    async def validate_file(self, file):
        if file.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")

    async def process_and_upload(self, file, request_id, uploads_dir):
        file_location = os.path.join(uploads_dir, file.filename)
        s3_key = f"/{request_id}_{file.filename}"
        with open(file_location, "wb") as file_object:
            content = file.file.read()
            # content = file.read()  # Consider using async if applicable
            file_object.write(content)
        s3_client.upload_file(file_location, BUCKET_RAGQA, s3_key)
        return file_location, s3_key

    async def ingest_document(self, file, request_id, uploads_dir, callback_url: str = None):
        await self.validate_file(file)
        _, s3_key = await self.process_and_upload(file, request_id, uploads_dir)
        logger.info("Uploaded file to S3: %s", file.filename)
        doc = self.repository.create_document(file.filename, s3_key, callback_url)
        uploaded_file = {
            'id': doc.id,
            "file_name": doc.title,
        }
        return uploaded_file

    async def trigger_processing_event(self, documents):
        for doc in documents:
            message = json.dumps({'document_id': doc["id"]})
            await self.redis_client.publish("document_processing", message)
            logger.info("Published document %s to Redis channel for processing", doc["id"])

    async def ingest_documents(self, files, callback_url: str = None):
        request_id = str(ULID())
        uploads_dir = os.path.join("/tmp/uploads/", request_id)
        os.makedirs(uploads_dir, exist_ok=True)

        uploaded_files = []

        try:
            for file in files:
                uploaded_file = await self.ingest_document(file, request_id, uploads_dir, callback_url)
                uploaded_files.append(uploaded_file)
            self.repository.commit()
            await self.trigger_processing_event(uploaded_files)
            return uploaded_files
        except Exception as e:
            logger.error("Error in document ingestion: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            shutil.rmtree(uploads_dir)
