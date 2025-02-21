# app/repositories/document_repository.py
from sqlalchemy.orm import Session
from database.models.document import Document
from typing import List

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, title: str, s3_key: str, callback_url: str = None) -> Document:
        doc = Document(title=title, s3_key=s3_key, callback_url=callback_url)
        self.db.add(doc)
        self.db.flush()
        return doc

    def get_all_documents(self, document_ids: List|None= None):
        base_query = self.db.query(Document)
        if document_ids:
            base_query = base_query.filter(Document.id.in_(document_ids))
        return base_query.all()

    def get_document_by_id(self, document_id):
        return self.db.query(Document).filter(Document.id == document_id).first()

    def commit(self):
        self.db.commit()
