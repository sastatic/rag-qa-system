# app/api/documents.py

from fastapi import APIRouter, UploadFile, File, Depends, Form
from typing import List, Optional
from sqlalchemy.orm import Session
from database.session import get_db
from repositories.document_repository import DocumentRepository
from services.document_service import DocumentService

router = APIRouter()

def get_document_service(db: Session = Depends(get_db)):
    return DocumentService(db)

@router.post("/", summary="Ingest new documents")
async def ingest_document(
    files: List[UploadFile] = File(...),
    callback_url: Optional[str] = Form(None),
    service: DocumentService = Depends(get_document_service)
):
    return await service.ingest_documents(files, callback_url)


@router.get("/", summary="Get all documents")
async def get_all_documents(db: Session = Depends(get_db)) -> List[dict]:
    documents = DocumentRepository(db).get_all_documents()
    response = []
    for doc in documents:
        response.append({
            "id": doc.id,
            "file_name": doc.title,
        })
    return response
