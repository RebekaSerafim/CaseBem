from fastapi import APIRouter, Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/prestador/dashboard")
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("prestador/dashboard.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/prestador/cadastar_servico")
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("prestador/cadastrar_servico.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/prestador/alterar_servico")
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("prestador/alterar_servico.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/prestador/excluir_servico")
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("prestador/excluir_servico.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/prestador/detalhes_do_servico")
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("prestador/detalhes_do_servico.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/prestador/dados_do_perfil")
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("prestador/dados_do_perfil.html", {"request": request, "usuario": usuario_logado})
    return response




