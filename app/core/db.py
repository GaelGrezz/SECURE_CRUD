import os
from dotenv import load_dotenv
import mysql.connector as conn 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine_kargs = {}
engine = create_engine(DATABASE_URL, 
    echo=True, # Desactivar en producción 
    future=True, 
    **engine_kargs)


session_local = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    class_=Session)

def test_sqlalchemy():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("Conexión lograda con SQLAlchemy: ", conn)
    except Exception as e:
        print("Error de origen: ", e)