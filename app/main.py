from dotenv import load_dotenv
from fastapi import FastAPI

from .api.router import router

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="SECURE CRUD")
    app.include_router(router)
    return app

app = create_app()