# app/api/qa.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.qa import Question, Answer
from services.qa_service import QAService
from database.session import get_db
from common import get_logger

logger = get_logger(__name__)
router = APIRouter()

def get_qa_service(db: Session = Depends(get_db)):
    return QAService(db)

@router.post("/", summary="Get answer for a question")
async def get_answer(question: Question, qa_service: QAService = Depends(get_qa_service)) -> Answer:
    logger.info("Recieved request for a question: %s", question.model_dump(exclude_none=True))
    answer: Answer = await qa_service.generate_answer(question)
    logger.info("Answer generated.")
    return answer
