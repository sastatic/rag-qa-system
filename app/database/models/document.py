from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from database.base import Base
from ulid import ULID
import enum


class DocumentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))
    title = Column(String, nullable=True)
    callback_url = Column(String, nullable=True)
    status = Column(String, default="pending")
    s3_key = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
