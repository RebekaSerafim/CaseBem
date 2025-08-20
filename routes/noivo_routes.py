from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/noivo/dashboard")
async def get_root():
    response = templates.TemplateResponse("noivo/dashboard.html", {"request": {}})
    return response

@router.get("/noivo/noivos")
async def get_root():
    response = templates.TemplateResponse("noivo/noivos.html", {"request": {}})
    return response

@router.get("/noivo/noivos/cadastrar")
async def get_root():
    response = templates.TemplateResponse("noivo/cadastrar_noivo.html", {"request": {}})
    return response

@router.get("/noivo/noivos/alterar/{id_noivo}")
async def get_root(id_noivo: int):
    response = templates.TemplateResponse("noivo/alterar_noivo.html", {"request": {}})
    return response

@router.get("/noivo/noivos/excluir/{id_noivo}")
async def get_root(id_noivo: int):
    response = templates.TemplateResponse("noivo/excluir_noivo.html", {"request": {}})
    return response

@router.get("/noivo/compras_e_contratacoes/{id_noivo}")
async def get_root(id_noivo: int):
    response = templates.TemplateResponse("noivo/compras_e_contratacoes.html", {"request": {}, "id_noivo": id_noivo})
    return response

@router.get("/noivo/dados_usuario/cadastrar")
async def get_root():
    response = templates.TemplateResponse("noivo/cadastrar_dados_usuario.html", {"request": {}})
    return response

