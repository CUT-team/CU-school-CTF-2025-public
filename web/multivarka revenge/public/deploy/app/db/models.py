import uuid
from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from .base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    table_name = Column(String, nullable=False)
    status = Column(String, default="pending")
    results = Column(JSON, nullable=True)
    message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    md5 = Column(String, nullable=False)