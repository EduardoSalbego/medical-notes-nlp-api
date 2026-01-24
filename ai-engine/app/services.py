import spacy
import re
from spacy.tokens import Span
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
        if "entity_ruler" not in self.nlp.pipe_names:
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
        
        entities = []
        for ent in doc.ents:
            entities.append(Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            ))

        cpf_pattern = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
        for match in re.finditer(cpf_pattern, text):
            entities.append(Entity(
                text=match.group(),
                label="PII_CPF",
                start=match.start(),
                end=match.end()
            ))

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        for match in re.finditer(email_pattern, text):
            entities.append(Entity(
                text=match.group(),
                label="PII_EMAIL",
                start=match.start(),
                end=match.end()
            ))

        return AnalysisResponse(
            status="success",
            entities=entities
        )

nlp_service = NLPService()