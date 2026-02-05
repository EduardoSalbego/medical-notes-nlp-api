import re
from typing import Dict, List, Tuple


class DataMaskingService:
    
    def __init__(self):
        self.patterns = {
            "cpf_br": r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}",
            "ssn_us": r"\d{3}-?\d{2}-?\d{4}",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone_br": r"(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}",
            "phone_us": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            "date": r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        }
    
    def mask_names(self, text: str) -> Tuple[str, List[str]]:
        name_patterns = [
            r"(?:Paciente|Patient|Sr\.|Sra\.|Dr\.|Dra\.)\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+)",
            r"([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+)\s+(?:presenta|apresenta|reports)",
        ]
        
        masked_names = []
        masked_text = text
        
        for pattern in name_patterns:
            matches = re.finditer(pattern, masked_text, re.IGNORECASE)
            for match in matches:
                name = match.group(1)
                if name not in masked_names:
                    masked_names.append(name)
                masked_text = masked_text.replace(name, "[PATIENT_NAME]")
        
        return masked_text, masked_names
    
    def mask_pii(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        masked_text = text
        removed_pii = {
            "cpfs": [],
            "ssns": [],
            "emails": [],
            "phones": [],
            "dates": []
        }
        
        cpfs = re.findall(self.patterns["cpf_br"], masked_text)
        if cpfs:
            removed_pii["cpfs"] = list(set(cpfs))
            masked_text = re.sub(self.patterns["cpf_br"], "[CPF]", masked_text)
        
        ssns = re.findall(self.patterns["ssn_us"], masked_text)
        if ssns:
            removed_pii["ssns"] = list(set(ssns))
            masked_text = re.sub(self.patterns["ssn_us"], "[SSN]", masked_text)
        
        emails = re.findall(self.patterns["email"], masked_text, re.IGNORECASE)
        if emails:
            removed_pii["emails"] = list(set(emails))
            masked_text = re.sub(self.patterns["email"], "[EMAIL]", masked_text, flags=re.IGNORECASE)
        
        phones_br = re.findall(self.patterns["phone_br"], masked_text)
        if phones_br:
            removed_pii["phones"].extend(phones_br)
            masked_text = re.sub(self.patterns["phone_br"], "[PHONE]", masked_text)
        
        phones_us = re.findall(self.patterns["phone_us"], masked_text)
        if phones_us:
            removed_pii["phones"].extend(phones_us)
            masked_text = re.sub(self.patterns["phone_us"], "[PHONE]", masked_text)
        
        dates = re.findall(self.patterns["date"], masked_text)
        removed_pii["dates"] = dates[:3]
        
        return masked_text, removed_pii
    
    def de_identify(self, text: str) -> Dict:
        text_after_names, names_removed = self.mask_names(text)
        
        final_text, pii_removed = self.mask_pii(text_after_names)
        
        return {
            "masked_text": final_text,
            "removed_entities": {
                "names": names_removed,
                "pii": pii_removed
            }
        }

data_masking_service = DataMaskingService()