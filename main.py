from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root():
    response = templates.TemplateResponse("home.html", {"request": {}})
    return response

@app.get("/produtoseservicos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos.html", {"request": {}})
    return response

@app.get("/produtoseservicos_vestidos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos_vestidos/produtoseservicos_vestidos.html", {"request": {}})
    return response

@app.get("/card_vestido1")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos_vestidos/card_vestido1.html", {"request": {}})
    return response

@app.get("/card_vestido2")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos_vestidos/card_vestido2.html", {"request": {}})
    return response

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
