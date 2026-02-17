import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

from .api.router import router

load_dotenv()

requests_log = {}

def create_app() -> FastAPI:
    app = FastAPI(title="SECURE CRUD")
    app.include_router(router)
    
    @app.middleware("http")
    async def rate_limiter(request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        if client_ip not in requests_log:
            requests_log[client_ip] = []
            
        requests_log[client_ip] = [t for t in requests_log[client_ip] if now -t < 10]
        requests_log[client_ip].append(now)
        
        if len(requests_log[client_ip]) > 2:
            raise HTTPException(status_code=429, detail="Muchos intentos realizados.")
        
        response = await call_next(request)
        return response
    
    return app

app = create_app()