from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Question, Answer
from services.qa_service import QAService
from database.session import get_db
from common import get_logger

logger = get_logger(__name__)
router = APIRouter()

def get_qa_service(db: Session = Depends(get_db)):
    return QAService(db)

@router.post("/", summary="Get answer for a question")
async def get_answer(
    question: Question,
    qa_service: QAService = Depends(get_qa_service)
):
    logger.info("Received request for a question: %s", question.model_dump(exclude_none=True))
    answer: Answer = await qa_service.generate_answer(question)
    logger.info("Generated answer's length is %s", len(answer.answer))
    return answer
