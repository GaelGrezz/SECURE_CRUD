from sqlalchemy import Table
from sqlalchemy.orm import Session
from core.db import get_DB
from models.schemas import M_CRUD, M_U_CRUD

class BaseCRUD:
    def __init__(self, table: Table, db: Session):
        self.db = db
        self.table = table
        
    def create(self, data:M_CRUD):
            """
            Crear registro validado por el modelo CRUD.
            """
            data = data.model_dump()
            self.db.execute(self.table.insert().values(**data))
            self.db.commit()
        
    def read(self):
            """
            Regresar registros.
            """
            query = self.table.select()
            return self.db.execute(query).fetchall()
        
    def update(self, s_text:str, data:M_U_CRUD):
            """
            Actualizar registros.
            """
            valores = {k: v for k, v in data.dict().items()() if v is not None}
            self.db.execute(self.table.update().where(self.table.c.text == s_text).values(**valores))
            self.db.commit()
        
    def delete(self, s_text:str):
            self.db.execute(self.table.update().where(self.table.c.text == s_text).values(status=0)) 
            self.db.commit()