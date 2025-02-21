from pydantic import BaseModel
from typing import List, Optional


class Question(BaseModel):
    query: str
    selected_document: Optional[List[str]] = []


class Answer(BaseModel):
    answer: str
