from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.core.crud import BaseCRUD
from app.core.db import get_DB, table_crud
from app.models.schemas import M_CRUD

router = APIRouter(prefix="/content", tags=["CRUD"])

@router.post("/", response_model=dict, response_description="Registro creado exitósamente", status_code=status.HTTP_201_CREATED)
def create(data: M_CRUD, db: Session = Depends(get_DB)):
    crud = BaseCRUD(table=table_crud, db=db)
    try:
        crud.create(data)
        return {"message": "Registro creado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=400, deetail= str(e))