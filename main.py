from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes import locador_routes 
from routes import usuario_routes
from routes import prestador_routes
from routes import fornecedor_routes
from routes import noivo_routes
from routes import public_routes

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(usuario_routes.router)
app.include_router(locador_routes.router)
app.include_router(noivo_routes.router)
app.include_router(prestador_routes.router)
app.include_router(fornecedor_routes.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
