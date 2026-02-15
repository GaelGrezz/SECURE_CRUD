import os
from dotenv import load_dotenv
import mysql.connector as conn 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine_kargs = {}
engine = create_engine(DATABASE_URL, 
    echo=True, # ! Desactivar en producción 
    future=True, 
    pool_pre_ping=True,
    pool_recycle=100,
    pool_timeout=30,
    pool_size = 5,
    max_overflow=10,
    **engine_kargs)


session_local = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False,
    expire_on_commit=True, 
    class_=Session)

def get_DB():
    db = session_local()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()

def test_sqlalchemy():
    try:
        with engine.connect() as conn:
            print("Conexión lograda en: ", conn)
    except Exception as e:
        print("Error")