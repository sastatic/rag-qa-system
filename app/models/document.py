from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional
from ulid import ULID


class Document(BaseModel):
    id: ULID = Field(default_factory=ULID)
    title: str
    content: Optional[datetime] = None
    callback_url: Optional[HttpUrl] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
