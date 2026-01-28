from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-engine",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/ready")
async def readiness_check():
    try:
        from app.services.nlp_processor import nlp_processor
        return {
            "status": "ready",
            "service": "ai-engine",
            "nlp_models": "loaded",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }