import datetime
from sqlalchemy import Column, String, DateTime
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
    title = Column(String, nullable=False)
    document_url = Column(String, nullable=False)
    status = Column(String, default=DocumentStatus.PENDING.value)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
