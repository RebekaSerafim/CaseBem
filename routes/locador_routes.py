from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/locador/dashboard")
async def get_root():
    response = templates.TemplateResponse("locador/dashboard.html", {"request": {}})
    return response

@router.get("/locador/locadores")
async def get_root():
    response = templates.TemplateResponse("locador/locadores.html", {"request": {}})
    return response

@router.get("/locador/locadores/cadastrar")
async def get_root():
    response = templates.TemplateResponse("locador/cadastrar_locador.html", {"request": {}})
    return response

@router.get("/locador/locadores/alterar/{id_locador}")
async def get_root(id_locador: int):
    response = templates.TemplateResponse("locador/alterar_locador.html", {"request": {}})
    return response

@router.get("/locador/locadores/excluir/{id_locador}")
async def get_root(id_locador: int):
    response = templates.TemplateResponse("locador/excluir_locador.html", {"request": {}})
    return response

@router.get("/locador/detalhes_local/{id_locador}")
async def get_root(id_locador: int):
    response = templates.TemplateResponse("locador/detalhes_local.html", {"request": {}, "id_locador": id_locador})
    return response

@router.get("/locador/dados_perfil/cadastrar")
async def get_root():
    response = templates.TemplateResponse("locador/cadastrar_dados_perfil.html", {"request": {}})
    return response

