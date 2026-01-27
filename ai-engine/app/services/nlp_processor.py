import spacy
import re
import time
from typing import Dict, List, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class NLPProcessor:
    
    def __init__(self):
        try:
            self.nlp_en = spacy.load("en_core_web_sm")
            self.nlp_pt = spacy.load("pt_core_news_sm")
            logger.info("NLP models loaded successfully")
        except OSError as e:
            logger.error(f"Error loading NLP models: {e}")
            logger.info("Attempting to download models...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            subprocess.run(["python", "-m", "spacy", "download", "pt_core_news_sm"])
            self.nlp_en = spacy.load("en_core_web_sm")
            self.nlp_pt = spacy.load("pt_core_news_sm")
    
    def detect_language(self, text: str) -> str:
        portuguese_chars = re.search(r'[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]', text)
        if portuguese_chars:
            return "pt"
        return "en"
    
    def extract_symptoms(self, doc, language: str) -> List[str]:
        symptoms = []
        
        symptom_patterns = {
            "en": [
                r"presents?\s+with\s+([^.,]+)",
                r"symptoms?\s+include[:\s]+([^.,]+)",
                r"complains?\s+of\s+([^.,]+)",
                r"reports?\s+([^.,]+)",
            ],
            "pt": [
                r"apresenta\s+([^.,]+)",
                r"sintomas?\s+incluem[:\s]+([^.,]+)",
                r"queixa[-\s]?se\s+de\s+([^.,]+)",
                r"relata\s+([^.,]+)",
            ]
        }
        
        text = doc.text.lower()
        patterns = symptom_patterns.get(language, symptom_patterns["en"])
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                symptom_text = match.group(1).strip()
                symptom_list = re.split(r'[,;]|\s+e\s+|\s+and\s+', symptom_text)
                symptoms.extend([s.strip() for s in symptom_list if s.strip()])
        
        for ent in doc.ents:
            if ent.label_ in ["SYMPTOM", "DISEASE", "CONDITION"]:
                symptoms.append(ent.text)
        
        symptoms = list(set([s.lower() for s in symptoms if len(s) > 2]))
    
    def extract_medications(self, doc, language: str) -> List[str]:
        medications = []
        
        medication_patterns = {
            "en": [
                r"prescribed?\s+([A-Z][a-z]+(?:\s+\d+\s*(?:mg|g|ml|tablets?|capsules?))?)",
                r"medication[:\s]+([^.,]+)",
                r"taking\s+([A-Z][a-z]+)",
                r"([A-Z][a-z]+\s+\d+\s*(?:mg|g|ml))",
            ],
            "pt": [
                r"prescrito\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+(?:\s+\d+\s*(?:mg|g|ml|comprimidos?|cápsulas?))?)",
                r"medica[çc][ãa]o[:\s]+([^.,]+)",
                r"tomando\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+)",
                r"([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+\s+\d+\s*(?:mg|g|ml))",
            ]
        }
        
        text = doc.text
        patterns = medication_patterns.get(language, medication_patterns["en"])
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                med = match.group(1).strip()
                if len(med) > 2:
                    medications.append(med)
        
        for ent in doc.ents:
            if ent.label_ in ["DRUG", "MEDICATION"]:
                medications.append(ent.text)
        
        medications = list(set(medications))
        return medications[:15]
    
    def extract_diagnoses(self, doc, language: str) -> List[str]:
        diagnoses = []
        
        diagnosis_patterns = {
            "en": [
                r"diagnosis[:\s]+([^.,]+)",
                r"diagnosed?\s+with\s+([^.,]+)",
                r"dx[:\s]+([^.,]+)",
            ],
            "pt": [
                r"diagn[óo]stico[:\s]+([^.,]+)",
                r"diagnosticado\s+com\s+([^.,]+)",
                r"diagnosticada\s+com\s+([^.,]+)",
            ]
        }
        
        text = doc.text
        patterns = diagnosis_patterns.get(language, diagnosis_patterns["en"])
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                diagnosis = match.group(1).strip()
                diagnoses.append(diagnosis)
        
        for ent in doc.ents:
            if ent.label_ in ["DISEASE", "CONDITION", "DIAGNOSIS"]:
                diagnoses.append(ent.text)
        
        diagnoses = list(set(diagnoses))
        return diagnoses[:10]
    
    def classify_risk(self, symptoms: List[str], diagnoses: List[str], text: str) -> Tuple[str, Dict[str, float]]:
        
        critical_keywords = {
            "en": ["cardiac arrest", "stroke", "seizure", "unconscious", "respiratory failure", 
                   "severe pain", "chest pain", "difficulty breathing", "anaphylaxis"],
            "pt": ["parada cardíaca", "avc", "convulsão", "inconsciente", "insuficiência respiratória",
                   "dor severa", "dor no peito", "dificuldade para respirar", "anafilaxia"]
        }
        
        high_keywords = {
            "en": ["high fever", "severe", "intense", "acute", "emergency", "urgent"],
            "pt": ["febre alta", "severa", "intensa", "aguda", "emergência", "urgente"]
        }
        
        moderate_keywords = {
            "en": ["moderate", "persistent", "recurrent"],
            "pt": ["moderada", "persistente", "recorrente"]
        }
        
        text_lower = text.lower()
        language = self.detect_language(text)
        
        keywords_dict = {
            "critical": critical_keywords.get(language, critical_keywords["en"]),
            "high": high_keywords.get(language, high_keywords["en"]),
            "moderate": moderate_keywords.get(language, moderate_keywords["en"])
        }
        
        scores = {
            "critical": 0.0,
            "high": 0.0,
            "moderate": 0.0,
            "low": 0.0
        }
        
        for keyword in keywords_dict["critical"]:
            if keyword.lower() in text_lower:
                scores["critical"] += 0.3
        
        for keyword in keywords_dict["high"]:
            if keyword.lower() in text_lower:
                scores["high"] += 0.2
        
        for keyword in keywords_dict["moderate"]:
            if keyword.lower() in text_lower:
                scores["moderate"] += 0.15
        
        symptom_count = len(symptoms)
        diagnosis_count = len(diagnoses)
        
        if symptom_count > 5 or diagnosis_count > 2:
            scores["high"] += 0.1
        elif symptom_count > 3 or diagnosis_count > 1:
            scores["moderate"] += 0.1
        else:
            scores["low"] += 0.1
        
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        else:
            scores["low"] = 1.0
        
        classification = max(scores, key=scores.get)
        
        return classification, scores
    
    def process(self, text: str) -> Dict:
        """Process medical note text and extract entities"""
        start_time = time.time()
        
        language = self.detect_language(text)
        nlp_model = self.nlp_pt if language == "pt" else self.nlp_en
        
        doc = nlp_model(text)
        
        symptoms = self.extract_symptoms(doc, language)
        medications = self.extract_medications(doc, language)
        diagnoses = self.extract_diagnoses(doc, language)
        
        risk_classification, confidence_scores = self.classify_risk(symptoms, diagnoses, text)
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            "entities": {
                "symptoms": symptoms,
                "medications": medications,
                "diagnoses": diagnoses
            },
            "risk_classification": risk_classification,
            "confidence_score": confidence_scores,
            "processing_time_ms": round(processing_time, 2),
            "language_detected": language
        }

nlp_processor = NLPProcessor()