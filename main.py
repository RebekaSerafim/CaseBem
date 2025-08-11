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
    response = templates.TemplateResponse("produtoseservicos.html", {"request": {}})
    return response

@app.get("/produtoseservicos_acessorios")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_acessorios.html", {"request": {}})
    return response

@app.get("/produtoseservicos_alianca")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_alianca.html", {"request": {}})
    return response

@app.get("/produtoseservicos_bolos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_bolos.html", {"request": {}})
    return response

@app.get("/produtoseservicos_bridalday")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_bridalday.html", {"request": {}})
    return response

@app.get("/produtoseservicos_buffet")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_buffet.html", {"request": {}})
    return response

@app.get("/produtoseservicos_cenografia_sonoplastia")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_cenografia_sonoplastia.html", {"request": {}})
    return response

@app.get("/produtoseservicos_convite")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_convite.html", {"request": {}})
    return response

@app.get("/produtoseservicos_florista")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_florista.html", {"request": {}})
    return response

@app.get("/produtoseservicos_fotografos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_fotografos.html", {"request": {}})
    return response

@app.get("/produtoseservicos_lembrancinhas")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_lembrancinhas.html", {"request": {}})
    return response

@app.get("/produtoseservicos_locais")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_locais.html", {"request": {}})
    return response

@app.get("/produtoseservicos_ternos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_ternos.html", {"request": {}})
    return response

@app.get("/produtoseservicos_vestidos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos_vestidos.html", {"request": {}})
    return response

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
