from datetime import datetime
import re
from abc import ABC
import uuid

from fastapi import HTTPException


class DataInsertSecurity(ABC):
    @staticmethod
    def validate_text(text: str):
        if not re.match(r'^[A-Za-zñÑ0-9\s.,!?-]+$', text):
            raise HTTPException(
                status_code=500, detail="El texto contiene carácteres no permitidos")

        forbidden = ["<script>", "</script>",
                     "javascript:", "onerror=", "onload="]
        for f in forbidden:
            if f.lower() in text.lower():
                raise HTTPException(
                    status_code=500, detail="Texto contiene patrones peligrosos")

            sql_keywords = ["drop", "delete", "insert",
                            "update", "select", "--", ";"]
            for kw in sql_keywords:
                if kw.lower() in text.lower():
                    raise HTTPException(
                        status_code=500, detail="Texto contiene palabras reservadas SQL")

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
    
    @staticmethod
    def validate_id(id_value: str):
        try:
            uuid_obj = uuid.UUID(id_value, version=4)
        except ValueError:
            raise HTTPException(status_code=422, detail="ID inválido: no es un formato permitido.")
        return str(uuid_obj)
    
    @staticmethod
    def validate_r_date(r_date):
        if not isinstance(r_date, datetime):
            raise HTTPException(
                status_code=423,
                detail="Fecha no aceptable: se espera una fecha."
            )
        if r_date > datetime.utcnow():
            raise HTTPException(
                status_code=423,
                detail="Fecha no aceptable: se espera una fecha actual."
            )
        return r_date