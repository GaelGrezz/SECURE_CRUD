from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.crud import BaseCRUD
from app.core.db import get_DB, table_crud
from app.models.schemas import M_CRUD, M_IP_CRUD, M_POST

router = APIRouter(prefix="/content", tags=["CRUD"])

@router.post("/", response_model=dict, response_description="Registro creado exitósamente", status_code=status.HTTP_201_CREATED)
def create(data: M_CRUD, request: Request, db: Session = Depends(get_DB)):
    crud = BaseCRUD(table=table_crud, db=db)
    try:
        clientIp = request.client.host
        crud.create(data, clientIp)
        return {"message": "Registro creado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail= str(e))

@router.put("/{id}", response_model=M_POST, response_description="Registro actualizado.")
def update(id: str, request: Request, data: M_POST, db: Session = Depends(get_DB)):
    crud = BaseCRUD(table_crud, db)
    
    try:
        crud.update(id, data, request.client.host)
    except ValidationError as e: 
        raise HTTPException(
            status_code=500, detail="No se ha logrado actualizar el post")

    return {"campo": "Registro actualizado"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_description="Registro eliminado")
def delete(id: str, request: Request, db: Session=Depends(get_DB)):
    crud = BaseCRUD(table=table_crud, db=db)
    try:
        crud.delete(id)
    except ValidationError as e:
        raise HTTPException(
            status_code=500, detail="No se ha logrado actualizar el post")

# @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_description="Post eliminado")
# def delete_post(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # repository = PostRepository(db)
    # post = repository.get(post_id)
    # if not post:
        # raise HTTPException(status_code=404, detail="Post no encontrado")
# 
    # try:
        # repository.delete_post(post)
        # db.commit()
    # except SQLAlchemyError:
        # db.rollback()
        # raise HTTPException(status_code=500, detail="Operación no lograda")
    # return
