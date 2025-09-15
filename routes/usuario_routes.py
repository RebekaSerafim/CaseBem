from fastapi import APIRouter, HTTPException, Request
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from repo import produto_repo
from fastapi import status
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/usuario/alterar_senha")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("usuario/alterar_senha.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/usuario/conversas")
@requer_autenticacao()
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("usuario/conversas.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/usuario/conversas/{id_conversa}")
@requer_autenticacao()
async def get_root(id_conversa: int, request: Request, usuario_logado: dict = None):    
    response = templates.TemplateResponse("usuario/chat.html", {"request": request, "usuario": usuario_logado})
    return response

@router.post("/produto/excluir/{id}")
@requer_autenticacao()
async def excluir_produto(id: int, usuario_logado: dict = None):
    # Verificar permissão adicional
    if usuario_logado['perfil'] != 'admin':
        raise HTTPException(403, "Apenas admins podem excluir produtos")
    
    produto_repo.excluir(id)
    return RedirectResponse("/produtos", status.HTTP_303_SEE_OTHER)