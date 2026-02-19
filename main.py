import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .app.api.router import router, sec_router

load_dotenv()

requests_log = {}

def create_app() -> FastAPI:
    app = FastAPI(title="SECURE CRUD")
    
    # 1. Rutas
    app.include_router(sec_router)
    app.include_router(router)
    
    # 2. Rate Limiter (Definido arriba para que se ejecute DESPUÉS del CORS)
    @app.middleware("http")
    async def rate_limiter(request: Request, call_next):
        client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0]

        print("Cliente IP: ", client_ip)
        if client_ip == "34.82.84.118" or request.method == "OPTIONS":
            return await call_next(request)
        
        now = time.time()
        if client_ip not in requests_log:
            requests_log[client_ip] = []
            
        requests_log[client_ip] = [t for t in requests_log[client_ip] if now - t < 10]
        requests_log[client_ip].append(now)
        
        if len(requests_log[client_ip]) > 2:
            raise HTTPException(status_code=429, detail="Muchos intentos realizados.")
        
        return await call_next(request)

    # 3. Tu CORS (Tal cual lo tenías, pero al FINAL del código)
    # Esto garantiza que sea lo PRIMERO que se ejecute al recibir la petición.
    origins = [
        "http://127.0.0.1:8000",
        "https://crud-villa-three.vercel.app"
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "auth"],
    )
    
    return app

app = create_app()
