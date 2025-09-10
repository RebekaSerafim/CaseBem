from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets

import uvicorn

from routes import auth_routes
from routes import cadastro_routes 
from routes import locador_routes
from routes import logout_route 
from routes import usuario_routes
from routes import prestador_routes
from routes import fornecedor_routes
from routes import noivo_routes
from routes import public_routes
from routes import auth_routes

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

app.include_router(public_routes.router)
app.include_router(usuario_routes.router)
app.include_router(locador_routes.router)
app.include_router(noivo_routes.router)
app.include_router(prestador_routes.router)
app.include_router(fornecedor_routes.router)
app.include_router(auth_routes.routesr)
app.include_router(cadastro_routes.router)
app.include_router(logout_route.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
