from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import hashlib
from app.services.nlp_processor import nlp_processor
from app.services.data_masking import data_masking_service
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.medical_note import MedicalNoteProcessing

router = APIRouter()

class MedicalNoteRequest(BaseModel):
    medical_note: str = Field(..., min_length=10, description="Medical note text to process")
    skip_masking: bool = Field(default=False, description="Skip data masking (not recommended)")
    note_hash: Optional[str] = Field(None, description="Optional hash for tracking")

class MedicalNoteResponse(BaseModel):
    status: str
    data: dict
    processed_at: datetime

@router.post("/process", response_model=MedicalNoteResponse)
async def process_medical_note(
    request: MedicalNoteRequest,
    db: Session = Depends(get_db)
):
    try:
        if not request.skip_masking:
            de_identified = data_masking_service.de_identify(request.medical_note)
            text_to_process = de_identified["masked_text"]
        else:
            text_to_process = request.medical_note
            de_identified = {"masked_text": request.medical_note, "removed_entities": {}}
        
        nlp_result = nlp_processor.process(text_to_process)
        
        note_hash = request.note_hash or hashlib.sha256(
            request.medical_note.encode()
        ).hexdigest()[:16]
        
        response_data = {
            "entities": nlp_result["entities"],
            "risk_classification": nlp_result["risk_classification"],
            "confidence_score": nlp_result["confidence_score"],
            "processing_time_ms": nlp_result["processing_time_ms"],
            "language_detected": nlp_result["language_detected"],
            "note_hash": note_hash,
            "masking_applied": not request.skip_masking,
            "removed_entities": de_identified.get("removed_entities", {})
        }
        
        try:
            processing_record = MedicalNoteProcessing(
                note_hash=note_hash,
                entities=nlp_result["entities"],
                risk_classification=nlp_result["risk_classification"],
                confidence_score=nlp_result["confidence_score"],
                raw_text=text_to_process,
                processing_time_ms=str(nlp_result["processing_time_ms"])
            )
            db.add(processing_record)
            db.commit()
        except Exception as e:
            print(f"Error storing processing record: {e}")
            db.rollback()
        
        return MedicalNoteResponse(
            status="success",
            data=response_data,
            processed_at=datetime.utcnow()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing medical note: {str(e)}"
        )

@router.get("/stats")
async def get_processing_stats(db: Session = Depends(get_db)):
    try:
        total_processed = db.query(MedicalNoteProcessing).count()
        
        risk_counts = {}
        for risk_level in ["low", "moderate", "high", "critical"]:
            count = db.query(MedicalNoteProcessing).filter(
                MedicalNoteProcessing.risk_classification == risk_level
            ).count()
            risk_counts[risk_level] = count
        
        return {
            "status": "success",
            "statistics": {
                "total_processed": total_processed,
                "by_risk_classification": risk_counts
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving statistics: {str(e)}"
        )