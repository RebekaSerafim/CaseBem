from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets
import os
from dotenv import load_dotenv

import uvicorn

# Carregar variáveis do arquivo .env
load_dotenv()

from routes import public_routes, admin_routes, fornecedor_routes, noivo_routes
from util.startup import inicializar_sistema

app = FastAPI()
SECRET_KEY = secrets.token_urlsafe(32)

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rotas
app.include_router(public_routes.router)
app.include_router(admin_routes.router)
app.include_router(fornecedor_routes.router)
app.include_router(noivo_routes.router)

# Inicializar sistema na primeira execução
@app.on_event("startup")
async def startup_event():
    inicializar_sistema()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
