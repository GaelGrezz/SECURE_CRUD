import os 
from dotenv import load_dotenv
import mysql.connector as conn 
from sqlalchemy import create_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def test_sqlalchemy():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("Conexión lograda con SQLAlchemy: ", conn)
    except Exception as e:
        print("Error de origen: ", e)

if __name__ == "__main__":
    test_sqlalchemy()
    