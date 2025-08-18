from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from routes import public_routes

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(public_routes.router)

@app.get("/contato_vestido1")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos_vestidos/contato_vestido1.html", {"request": {}})
    return response




if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
