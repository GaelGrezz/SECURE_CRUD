from models.schemas import M_CRUD
from core.db import get_DB, session_local, table_crud
from core.crud import BaseCRUD

def main ():
    db = session_local()
    try:
        crud = BaseCRUD(table=table_crud, db = db)
        registro = M_CRUD( text="SÉLECT * FROM user", status=True, ip="127.0.0.1" )
        crud.create(registro)
        rest = crud.read()
    except Exception as e:
        print("Error: ", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()