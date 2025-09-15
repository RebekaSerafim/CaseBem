from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/noivo/dashboard")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/dashboard.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/noivo/noivos")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/noivos.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/noivo/noivos/cadastrar")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/cadastrar_noivo.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/noivo/noivos/alterar/{id_noivo}")
@requer_autenticacao()
async def get_root(id_noivo: int, request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/alterar_noivo.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/noivo/noivos/excluir/{id_noivo}")
@requer_autenticacao()
async def get_root(id_noivo: int, request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/excluir_noivo.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/noivo/compras_e_contratacoes/{id_noivo}")
@requer_autenticacao()
async def get_root(id_noivo: int, request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/compras_e_contratacoes.html", {"request": request, "id_noivo": id_noivo, "usuario": usuario_logado})
    return response

@router.get("/noivo/dados_usuario/cadastrar")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("noivo/cadastrar_dados_usuario.html", {"request": request, "usuario": usuario_logado})
    return response

