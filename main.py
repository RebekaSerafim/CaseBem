from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes import public_routes
from routes import usuario_routes

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(usuario_routes.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
