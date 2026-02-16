from pydantic import BaseModel, Field, field_validator

class CRUD(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        min_length=50,
        description="Contenido de la entrada, con un rango permitido entre 10 a 50 dígitos.",
        # todo: Evitar inyecciones de carácteres peligrosos o sqlinyección
        regex=r'^[A-Za-z0-9\s.,!?-]+$',
        examples=["Contenido válido con el rango permitido"]
    )
    
    class Config(BaseModel):
        anystr_strip_whitespace = True
        extra = "forbid"
        
    @field_validator("text") 
    def check_forbidden_patterns(cls, value): 
        # Bloquear intentos de XSS 
        forbidden = ["<script>", "</script>", "javascript:", "onerror=", "onload="] 
        for f in forbidden: 
            if f.lower() in value.lower(): 
                raise ValueError("Texto contiene patrones peligrosos")
        return value
    
    @field_validator("text") 
    def sanitize_sql_injection(cls, value): 
        # Bloquear intentos básicos de SQL injection 
        sql_keywords = ["drop", "delete", "insert", "update", "select", "--", ";"] 
        for kw in sql_keywords: 
            if kw.lower() in value.lower(): 
                raise ValueError("Texto contiene palabras reservadas SQL") 
        return value
