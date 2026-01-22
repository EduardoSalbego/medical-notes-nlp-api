import spacy
from spacy.pipeline import EntityRuler
from app.schemas import AnalysisResponse, Entity

class NLPService:
    def __init__(self):
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            spacy.cli.download("pt_core_news_sm")
            self.nlp = spacy.load("pt_core_news_sm")

        self._add_medical_ruler()

    def _add_medical_ruler(self):
        ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        
        patterns = [
            {"label": "MEDICAMENTO", "pattern": [{"LOWER": "dipirona"}]},
            {"label": "MEDICAMENTO", "pattern": [{"LOWER": "amoxicilina"}]},
            {"label": "SINTOMA", "pattern": [{"LOWER": "febre"}]},
            {"label": "SINTOMA", "pattern": [{"LOWER": "cefaleia"}]},
            {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "hipertensao"}]},
            {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "diabetes"}]}
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