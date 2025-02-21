# app/services/document_processor.py

import os
import shutil
import httpx
from datetime import datetime
from typing import Optional
from llama_index.core.embeddings import resolve_embed_model
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from database.models.document import Document, DocumentStatus
from database.session import get_db
from database import create_s3_client
from common import get_logger
from common.config import BUCKET_RAGQA, EMBED_MODEL
from repositories.document_repository import DocumentRepository

logger = get_logger(__name__)

class DocumentProcessor:
    def __init__(self, db, s3_client, embed_model, file_extractor: dict):
        self.db = db
        self.s3_client = s3_client
        self.embed_model = embed_model
        self.file_extractor = file_extractor
        self.logger = logger
        self.document_repo = DocumentRepository(db)

    async def send_webhook_notification(self, document: Document):
        if not document.callback_url:
            self.logger.info("Callback URL not provided")
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    document.callback_url,
                    json={
                        "status": document.status,
                        "file_name": document.title,
                        "processed_at": document.updated_at.isoformat() if document.updated_at else None,
                    },
                )
                response.raise_for_status()
                self.logger.info("Successfully sent webhook notification.")
            except Exception as e:
                self.logger.error("Failed to send webhook notification: %s", str(e))

    async def process_document(self, document_id: str):
        document: Optional[Document] = self.document_repo.get_document_by_id(document_id)
        if not document:
            self.logger.exception("document_id: %s not found", document_id)
            return

        download_dir = os.path.join("/tmp/downloads", str(document.id))
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, document.title)

        try:
            # Download file from S3. (Note: This remains synchronous; consider using an executor if needed.)
            with open(file_path, "wb") as f:
                self.s3_client.download_fileobj(BUCKET_RAGQA, document.s3_key, f)

            # Use the file extension to choose a parser via our extractor strategy.
            ext = os.path.splitext(document.title)[1].lower()
            parser = self.file_extractor.get(ext)
            if parser is None:
                self.logger.error("No parser found for extension: %s", ext)
                document.status = DocumentStatus.FAILED.value
            else:
                # Process the document.
                reader = SimpleDirectoryReader(download_dir)
                docs = reader.load_data(show_progress=True)
                if docs:
                    doc = docs[0]
                    document.content = doc.text
                    document.embedding = self.embed_model.get_text_embedding(document.content)
                    document.status = DocumentStatus.PROCESSED.value
                    document.updated_at = datetime.utcnow()
                else:
                    self.logger.error("No document data extracted.")
                    document.status = DocumentStatus.FAILED.value

            self.db.commit()
            self.db.refresh(document)
            self.logger.info("Successfully completed processing file: %s", document.title)

        except Exception as e:
            document.status = DocumentStatus.FAILED.value
            document.updated_at = datetime.utcnow()
            self.db.commit()
            self.logger.error("Error processing file %s: %s", document.title, str(e))

        finally:
            await self.send_webhook_notification(document)
            try:
                shutil.rmtree(download_dir)
                self.logger.info("Successfully cleaned up: %s", download_dir)
            except Exception as e:
                self.logger.warning("Failed to remove directory %s: %s", download_dir, str(e))


def get_document_processor():
    db = next(get_db())
    s3_client = create_s3_client()
    embed_model = resolve_embed_model(embed_model=EMBED_MODEL)
    pdf_parser = LlamaParse(result_type="markdown")
    file_extractor = {".pdf": pdf_parser}
    return DocumentProcessor(db, s3_client, embed_model, file_extractor)