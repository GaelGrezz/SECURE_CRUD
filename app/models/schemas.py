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
        examples=["Contenido válido con el rango permitido"]
    )
    
    status: StrictInt = Field(
        ...,
        description="Estado lógico del registro (1 = activo, 0 = inactivo)."
    )
    
    ip: IPvAnyAddress = Field(
        ...,
        description="Dirección IP del cliente que genera el registro.",
        examples=["127.0.0.1"]
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

    # Validación de status 
    @field_validator("status")
    def validate_status(cls, value):
        if value not in (0, 1):
            raise ValueError("Status inválido: debe ser 0 o 1")
        return value

    @field_serializer('ip')
    def serializer_ip(self, ip):
        return str(ip)

class M_U_CRUD(M_CRUD):
    pass

class M_UUID(BaseModel):
    id: UUID

class M_POST(BaseModel):
    id: UUID
    text: str