from pydantic import BaseModel
from typing import List, Optional
from ulid import ULID

class Question(BaseModel):
    query: str
    selected_document_ids: Optional[List[ULID]] = None

class Answer(BaseModel):
    answer: str
    relevant_documents: Optional[List[ULID]] = None