from sqlalchemy import Column, String, DateTime, JSON, Text
from datetime import datetime
from app.database import Base
import uuid


class MedicalNoteProcessing(Base):
    __tablename__ = "medical_note_processings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    note_hash = Column(String, index=True)
    entities = Column(JSON)
    risk_classification = Column(String)
    confidence_score = Column(JSON)
    raw_text = Column(Text)
    processed_at = Column(DateTime, default=datetime.utcnow)
    processing_time_ms = Column(String)