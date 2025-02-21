import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from sqlalchemy.orm import Session
from ulid import ULID
from database.models.document import Document, DocumentStatus
from database.session import get_db

router = APIRouter()

def save_file(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

@router.post("/", summary="Ingest a new document")
async def ingest_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    file_location = os.path.join(uploads_dir, file.filename)
    background_tasks.add_task(save_file, file, file_location)

    new_doc = Document(
        id=str(ULID()),
        title=title,
        content_url=file_location,
        status=DocumentStatus.PENDING.value,
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {
        "document_id": new_doc.id,
        "title": new_doc.title,
        "content_url": new_doc.content_url,
        "status": new_doc.status
    }

@router.get("/", summary="List all documents")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents
