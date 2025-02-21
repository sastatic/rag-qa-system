# app/api/qa.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.qa import Question, Answer
from services.qa_service import QAService
from database.session import get_db

router = APIRouter()

def get_qa_service(db: Session = Depends(get_db)):
    return QAService(db)

@router.post("/", summary="Get answer for a question")
async def get_answer(question: Question, qa_service: QAService = Depends(get_qa_service)) -> Answer:
    return await qa_service.generate_answer(question)
