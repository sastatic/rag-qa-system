from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ulid import ULID

class Document(BaseModel):
    id: ULID = Field(default_factory=ULID)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)