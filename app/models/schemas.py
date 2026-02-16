import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


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
    
    status: int = Field(
        ...,
        description="Estado lógico del registro (1 = activo, 0 = inactivo)."
    )
    
    ip: str = Field(
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
            raise ValueError("El campo 'status' solo puede ser 0 o 1") 
        return value

    # Validación de IP 
    @field_validator("ip") 
    def validate_ip(cls, value): 
        ip_pattern = re.compile( r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$" ) 
        if not ip_pattern.match(value): 
            raise ValueError("Formato de IP inválido") 
        # Validar que cada octeto esté en rango 0-255 
        octetos = value.split(".") 
        if any(int(o) < 0 or int(o) > 255 for o in octetos): 
            raise ValueError("Cada octeto de la IP debe estar entre 0 y 255") 
        return value

class M_U_CRUD(M_CRUD):
    text: Optional[str] = Field(None, min_length=10, max_length=50, pattern=r'^[A-Za-z0-9\s.,!?-]+$')
