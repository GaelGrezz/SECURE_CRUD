from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, Request
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..core.crud import BaseCRUD
from ..core.db import get_DB, table_crud
from ..utils.service_key import create_access_token, verify_token
from ..models.schemas import M_CRUD, M_IP_CRUD, M_POST, M_R_CRUD

router = APIRouter(prefix="/content", tags=["CRUD"])
sec_router = APIRouter(prefix="/secure/content", tags=["SCURE"])
oauth2_scheme = APIKeyHeader(name="Authorization")

@sec_router.post("/token")
def get_token():
    token = create_access_token()
    return {"access_token": token, 
            "token_type": "bearer"}

@sec_router.get("/secure-endpoint")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    client = verify_token(token)
    if client is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")
    return {"message": f"Acceso permitido para {client}"}

@router.post("/", response_model=dict, response_description="Registro creado exitósamente", status_code=status.HTTP_201_CREATED)
def create(
    data: M_CRUD, 
    request: Request, 
    client: str = Depends(verify_token), 
    db: Session = Depends(get_DB)):
    crud = BaseCRUD(table=table_crud, db=db)
    try:
        clientIp = request.client.host
        crud.create(data, clientIp)
        return {"message": "Registro creado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail= str(e))

@router.get("/registros", response_model=List[M_R_CRUD])
def read(client: str = Depends(verify_token), db: Session  = Depends(get_DB)):
    crud = BaseCRUD(table=table_crud, db=db)
    results = crud.read()
    return results

@router.put("/{id}", response_model=M_POST, response_description="Registro actualizado.")
def update(id: str, request: Request, data: M_POST, client: str = Depends(verify_token), db: Session = Depends(get_DB)):
    crud = BaseCRUD(table_crud, db)
    
    try:
        crud.update(id, data, request.client.host)
    except ValidationError as e: 
        raise HTTPException(
            status_code=500, detail="No se ha logrado actualizar el post")

    return {"campo": "Registro actualizado"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_description="Registro eliminado")
def delete(id: str, request: Request,  client: str = Depends(verify_token), db: Session=Depends(get_DB)):
    crud = BaseCRUD(table=table_crud, db=db)
    try:
        crud.delete(id)
    except ValidationError as e:
        raise HTTPException(
            status_code=500, detail="No se ha logrado actualizar el post")