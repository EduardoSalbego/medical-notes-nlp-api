import spacy
import re
from spacy.pipeline import EntityRuler
from app.schemas import AnalysisResponse, Entity

class NLPService:
    def __init__(self):
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            spacy.cli.download("pt_core_news_sm")
            self.nlp = spacy.load("pt_core_news_sm")

        self._add_rules()

    def _add_rules(self):
        ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        
        patterns = [
            {"label": "MEDICAMENTO", "pattern": [{"LOWER": "dipirona"}]},
            {"label": "MEDICAMENTO", "pattern": [{"LOWER": "amoxicilina"}]},
            {"label": "SINTOMA", "pattern": [{"LOWER": "febre"}]},
            {"label": "SINTOMA", "pattern": [{"LOWER": "cefaleia"}]},
            {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "hipertensao"}]},
            {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "diabetes"}]},
            {"label": "PII_CPF", "pattern": [{"TEXT": {"REGEX": r"\d{3}\.\d{3}\.\d{3}-\d{2}"}}]},
            {"label": "PII_EMAIL", "pattern": [{"TEXT": {"REGEX": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}]}
        ]
        
        ruler.add_patterns(patterns)

    def process_text(self, text: str) -> AnalysisResponse:
        doc = self.nlp(text)
        
        detected_entities = []
        for ent in doc.ents:
            detected_entities.append(Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            ))

        return AnalysisResponse(
            status="success",
            entities=detected_entities
        )

nlp_service = NLPService()