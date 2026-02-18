import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router, sec_router

load_dotenv()

requests_log = {}

def create_app() -> FastAPI:
    app = FastAPI(title="SECURE CRUD")
    
    # 1. Rutas
    app.include_router(sec_router)
    app.include_router(router)
    
    # 2. CORS - Añadimos OPTIONS a los métodos permitidos
    origins = [
        "http://127.0.0.1:8000",
        "https://crud-villa-three.vercel.app"
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], # <-- Crucial para el navegador
        allow_headers=["Authorization", "Content-Type"],
    )
    
    # 3. Rate Limiter mejorado
    @app.middleware("http")
    async def rate_limiter(request: Request, call_next):
        # SEGURIDAD: Obtenemos la IP real del usuario.
        # En Render, request.client.host es la IP del servidor interno, no la del usuario.
        # X-Forwarded-For nos da la IP real del atacante.
        client_ip = request.headers.get("X-Forwarded-For", request.client.host).split(",")[0]
        
        # Saltamos el límite en local
        if client_ip == "127.0.0.1":
            return await call_next(request)
        
        # SEGURIDAD: No bloqueamos OPTIONS. 
        # Es solo una consulta de permisos del navegador, no toca tus datos.
        if request.method == "OPTIONS":
            return await call_next(request)
        
        now = time.time()
        
        if client_ip not in requests_log:
            requests_log[client_ip] = []
            
        # Limpiamos logs de más de 10 segundos
        requests_log[client_ip] = [t for t in requests_log[client_ip] if now - t < 10]
        requests_log[client_ip].append(now)
        
        # Bloqueamos si hay más de 2 peticiones reales en 10 segundos
        if len(requests_log[client_ip]) > 2:
            raise HTTPException(status_code=429, detail="Muchos intentos realizados.")
        
        response = await call_next(request)
        return response
    
    return app

app = create_app()