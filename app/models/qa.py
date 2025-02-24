from pydantic import BaseModel, Field
from typing import List


class Question(BaseModel):
    query: str = Field(..., min_length=1)
    selected_document: List[str]|None = None


class Answer(BaseModel):
    answer: str
