from pydantic import ValidationError
from sqlalchemy import Table
from sqlalchemy.orm import Session

from utils.u_d_segurity import DataUDSecurity
from utils.c_segurity import DataInsertSecurity
from models.schemas import M_CRUD, M_U_CRUD, M_UUID

from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


class BaseCRUD:
    def __init__(self, table: Table, db: Session):
        self.db = db
        self.table = table

    def create(self, data: M_CRUD):
        try:
            """
            Crear registro validado por el modelo CRUD.
            """
            data = data.model_dump()

            data["text"] = DataInsertSecurity.canonicalize_text(data["text"])

            DataInsertSecurity.validate_text(data["text"])
            DataInsertSecurity.validate_status(data["status"])
            DataInsertSecurity.validate_ip(data["ip"])

            self.db.execute(self.table.insert().values(**data))
            self.db.commit()
        except ValidationError as pydnticErr:
            raise pydnticErr
        except (ValueError, SQLAlchemyError) as e:
            self.db.rollback()
            raise e

    def read(self):
        """
        Regresar registros.
        """
        query = self.table.select()
        return self.db.execute(query).fetchall()

    def update(self, r_id: M_UUID, data: M_U_CRUD):
    #     """
    #     Actualizar registros.
    #     """
        if not data:
            raise ValueError("No se han proporcionado datos para actualizar.")
        
        if not r_id:
            raise ValueError("No se ha proporcionado una ID para actualizar.")

        data = data.model_dump(exclude_unset=True)

        data["text"] = DataInsertSecurity.canonicalize_text(data["text"])

        DataInsertSecurity.validate_text(data["text"])
        DataInsertSecurity.validate_status(data["status"])
        DataInsertSecurity.validate_ip(data["ip"])

        query = (
            self.table.update()
            .where(self.table.c.id == str(UUID(r_id)))
            .values(**data)
        )

        try:
            self.db.execute(query)
            self.db.commit()
        except ValueError:
            raise ValueError("El ID proporcionado no es un UUID.")
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, r_id:M_UUID):
        self.db.execute(self.table.update().where(
            self.table.c.id == str(UUID(r_id))).values(status=0))
        self.db.commit()
