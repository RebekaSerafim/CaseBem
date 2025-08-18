from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root():
    response = templates.TemplateResponse("home.html", {"request": {}})
    return response

@router.get("/produtos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos.html", {"request": {}})
    return response

@router.get("/produtoseservicos_vestidos")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos_vestidos/produtoseservicos_vestidos.html", {"request": {}})
    return response

@router.get("/card_vestido1")
async def get_root():
    response = templates.TemplateResponse("produtoseservicos/produtoseservicos_vestidos/card_vestido1.html", {"request": {}})
    return response

@router.get("/sobre")
async def get_root():
    response = templates.TemplateResponse("sobre.html", {"request": {}})
    return response
