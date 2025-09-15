from fastapi import APIRouter, Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/fornecedor/dashboard")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("fornecedor/dashboard.html",  {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/fornecedor/cadastar_produto")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("fornecedor/cadastrar_produto.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/fornecedor/alterar_produto")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("fornecedor/alterar_produto.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/fornecedor/excluir_produto")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("fornecedor/excluir_produto.html",  {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/fornecedor/detalhes_do_produto")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("fornecedor/detalhes_do_produto.html", {"request": request, "usuario": usuario_logado}
    )
    return response

@router.get("/fornecedor/dados_do_perfil")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("fornecedor/dados_do_perfil.html", {"request": request, "usuario": usuario_logado}
    )
    return response




