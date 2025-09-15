from fastapi import APIRouter, Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/locador/dashboard")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/dashboard.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/locador/locadores")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/locadores.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/locador/locadores/cadastrar")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/cadastrar_locador.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/locador/locadores/alterar/{id_locador}")
@requer_autenticacao()
async def get_root(id_locador: int, request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/alterar_locador.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/locador/locadores/excluir/{id_locador}")
@requer_autenticacao()
async def get_root(id_locador: int, request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/excluir_locador.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/locador/detalhes_local/{id_locador}")
@requer_autenticacao()
async def get_root(id_locador: int, request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/detalhes_local.html", {"request": request, "usuario": usuario_logado}
    , "id_locador": id_locador)
    return response

@router.get("/locador/dados_perfil/cadastrar")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("locador/cadastrar_dados_perfil.html", {"request": request, "usuario": usuario_logado}
    )
    return response

