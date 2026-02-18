from datetime import datetime
import uuid
from pydantic import ValidationError
from sqlalchemy import Table, select
from sqlalchemy.orm import Session

from ..utils.enc_segurity import DataEncryptionService
from ..utils.c_segurity import DataInsertSecurity
from ..models.schemas import  M_IP_CRUD, M_R_CRUD, M_U_CRUD, M_UUID

from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


class BaseCRUD:
    def __init__(self, table: Table, db: Session):
        self.db = db
        self.table = table

    def create(self, data: M_U_CRUD, ip: M_IP_CRUD):
        try:
            """
            Crear registro validado por el modelo CRUD.
            """
            data = data.model_dump()

            data["id"] = str(uuid.uuid4())

            data["r_date"] = datetime.utcnow()
            
            data["ip"] = ip
            data["status"] = 1

            data["id"] = DataInsertSecurity.validate_id(data["id"])
            data["text"] = DataInsertSecurity.canonicalize_text(data["text"])
            DataInsertSecurity.validate_text(data["text"])
            DataInsertSecurity.validate_ip(data["ip"])
            data
            DataInsertSecurity.validate_r_date(data["r_date"])

            # ! Cifrado
            data["text"] = DataEncryptionService.encrypt(data["text"])
            print(data["text"])
            data["ip"] = DataEncryptionService.encrypt(data["ip"])

            self.db.execute(self.table.insert().values(**data))
            self.db.commit()
        except ValidationError as pydnticErr:
            raise pydnticErr
        except (ValueError, SQLAlchemyError) as e:
            self.db.rollback()
            raise e

    def read(self) -> list[M_R_CRUD]:
        """
        Regresar registros.
        """
        query = (
            select(self.table.c.id, self.table.c.text).where(self.table.c.status ==1)
        )
        result = self.db.execute(query).fetchall()
        
        return [
            M_R_CRUD(
                id=row.id, 
                contenido=DataEncryptionService.stc_decrypt(row.text)
                ) for row in result
        ]

    def update(self, r_id: M_UUID, data: M_U_CRUD, ip: M_IP_CRUD):
    #     """
    #     Actualizar registros.
    #     """
        if not data:
            raise ValueError("No se han proporcionado datos para actualizar.")
        
        if not r_id:
            raise ValueError("No se ha proporcionado una ID para actualizar.")

        data = data.model_dump(exclude_unset=True)
        data["ip"] = ip

        data["text"] = DataInsertSecurity.canonicalize_text(data["text"])
        DataInsertSecurity.validate_text(data["text"])
        DataInsertSecurity.validate_ip(data["ip"])

        data["text"] = DataEncryptionService.encrypt(data["text"])
        data["ip"] = DataEncryptionService.encrypt(data["ip"])

        query = (
            self.table.update()
            .where(self.table.c.id == r_id)
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
