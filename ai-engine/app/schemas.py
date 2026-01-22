from pydantic import BaseModel, Field
from typing import List

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, description="O texto médico para analisar")

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int

class AnalysisResponse(BaseModel):
    status: str
    entities: List[Entity]
    risk_score: str = "TBD"