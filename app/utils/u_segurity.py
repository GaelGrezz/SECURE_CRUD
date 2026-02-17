from abc import ABC
import re


class DataInsertSecurity(ABC):
    @staticmethod
    def validate_text(text:str):
        if not re.match(r'^[A-Za-z0-9\s.,!?-]+$', text):
            raise ValueError("Texto contiene caracteres no permitidos")
        forbidden = ["<script>", "</script>", "javascript:", "onerror=", "onload="]
        for f in forbidden:
            if f.lower() in text.lower(): 
                raise ValueError("Texto contiene patrones peligrosos") 
            sql_keywords = ["drop", "delete", "insert", "update", "select", "--", ";"] 
            for kw in sql_keywords: 
                if kw.lower() in text.lower(): 
                    raise ValueError