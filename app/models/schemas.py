import re
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, StrictInt, field_serializer, field_validator, IPvAnyAddress

class M_CRUD(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=50,
        description="Contenido de la entrada, con un rango permitido entre 10 a 50 dígitos.",
        # todo: Evitar inyecciones de carácteres peligrosos o sqlinyección
        pattern=r'^[A-Za-z0-9\s.,!?-]+$',
        examples=["Contenido permitido con el rango aceptable"],
        alias="campo"
    )
    
    model_config = {
        "str_strip_whitespace": True,
        "extra": "forbid"
    }

    @field_validator("text")
    def check_forbidden_patterns(cls, value):
        # Bloquear intentos de XSS
        forbidden = ["<script>", "</script>",
                     "javascript:", "onerror=", "onload="]
        for f in forbidden:
            if f.lower() in value.lower():
                raise ValueError("Texto contiene patrones peligrosos")
        return value

    @field_validator("text")
    def sanitize_sql_injection(cls, value):
        # Bloquear intentos básicos de SQL injection
        sql_keywords = ["drop", "delete", "insert",
                        "update", "select", "--", ";"]
        for kw in sql_keywords:
            if kw.lower() in value.lower():
                raise ValueError("Texto contiene palabras reservadas SQL")
        return value

class M_U_CRUD(M_CRUD):
    pass

class M_IP_CRUD(BaseModel):
    ip: IPvAnyAddress = Field(
        ...,
        description="Dirección IP del cliente que genera el registro.",
        examples=["127.0.0.1"],
        alias="campo ip cd"
    )
    
    
    @field_serializer('ip')
    def serializer_ip(self, ip):
        return str(ip)


class M_UUID(BaseModel):
    id: UUID

class M_POST(BaseModel):
    id: UUID
    text: str