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

        self._add_medical_ruler()

    def _add_medical_ruler(self):
        if "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            
            patterns = [
                {"label": "MEDICAMENTO", "pattern": [{"LOWER": "dipirona"}]},
                {"label": "MEDICAMENTO", "pattern": [{"LOWER": "amoxicilina"}]},
                {"label": "MEDICAMENTO", "pattern": [{"LOWER": "paracetamol"}]},
                {"label": "MEDICAMENTO", "pattern": [{"LOWER": "ibuprofeno"}]},
                {"label": "MEDICAMENTO", "pattern": [{"LOWER": "insulina"}]},
                {"label": "MEDICAMENTO", "pattern": [{"LOWER": "omeprazol"}]},
                
                {"label": "SINTOMA", "pattern": [{"LOWER": "febre"}]},
                {"label": "SINTOMA", "pattern": [{"LOWER": "cefaleia"}]},
                {"label": "SINTOMA", "pattern": [{"LOWER": "tosse"}]},
                {"label": "SINTOMA", "pattern": [{"LOWER": "nausea"}]},
                {"label": "SINTOMA", "pattern": [{"LOWER": "fadiga"}]},
                
                {"label": "SINTOMA_GRAVE", "pattern": [{"LOWER": "dispneia"}]},
                {"label": "SINTOMA_GRAVE", "pattern": [{"LOWER": "convulsao"}]},
                {"label": "SINTOMA_GRAVE", "pattern": [{"LOWER": "hemorragia"}]},
                {"label": "SINTOMA_GRAVE", "pattern": [{"LOWER": "cianose"}]},
                {"label": "SINTOMA_GRAVE", "pattern": [{"LOWER": "desmaio"}]},
                {"label": "SINTOMA_GRAVE", "pattern": [{"LOWER": "dor"}, {"LOWER": "no"}, {"LOWER": "peito"}]},
                
                {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "hipertensao"}]},
                {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "diabetes"}]},
                {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "pneumonia"}]},
                {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "infarto"}]},
                {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "avc"}]},
                {"label": "DIAGNOSTICO", "pattern": [{"LOWER": "asma"}]}
            ]
            
            ruler.add_patterns(patterns)

    def _calculate_risk(self, entities):
        score = 0
        for ent in entities:
            if ent.label == "SINTOMA_GRAVE":
                score += 50
            elif ent.label == "DIAGNOSTICO":
                score += 20
            elif ent.label == "SINTOMA":
                score += 10
        
        if score >= 50:
            return "High"
        if score >= 20:
            return "Medium"
        return "Low"

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

        risk_level = self._calculate_risk(entities)

        return AnalysisResponse(
            status="success",
            entities=entities,
            risk_score=risk_level
        )

nlp_service = NLPService()