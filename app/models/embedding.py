from pydantic import BaseModel
from typing import List
from ulid import ULID

class Embedding(BaseModel):
    document_id: ULID
    vector: List[float]