import re
from abc import ABC

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
                    raise ValueError("Texto contiene palabras reservadas SQL")
    @staticmethod 
    def validate_status(status: int): 
        if status not in (0, 1): 
            raise ValueError("Status inválido: debe ser 0 o 1") 
    @staticmethod 
    def validate_ip(ip: str): 
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$") 
        if not ip_pattern.match(ip): 
            raise ValueError("Formato de IP inválido") 
        octetos = ip.split(".") 
        if any(int(o) < 0 or int(o) > 255 for o in octetos): 
            raise ValueError("Cada octeto de la IP debe estar entre 0 y 255")
        
    @staticmethod
    def canonicalize_text(text: str) -> str:
        """ 
        Limpieza y normalización de texto: 
            - Elimina espacios al inicio y al final 
            - Reduce espacios múltiples 
            - Elimina saltos de línea/tabulaciones 
        """
        if not isinstance(text, str):
            raise ValueError("El campo debe ser una cadena de texto.")
        
        cleaned = text.strip()
        cleaned = " ".join(cleaned.split())
        return cleaned