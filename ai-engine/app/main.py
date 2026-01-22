from fastapi import FastAPI
from app.schemas import AnalysisRequest, AnalysisResponse
from app.services import nlp_service

app = FastAPI(title="Medical NLP Engine")

@app.get("/")
def health_check():
    return {"status": "online", "service": "medical-notes-ai"}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_medical_note(request: AnalysisRequest):
    """
    Recebe um texto médico bruto e retorna entidades extraídas.
    """
    result = nlp_service.process_text(request.text)
    return result