from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/dashboard")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/dashboard.html", {"request": request})
    return response

@router.get("/administrador/administradores")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/administradores.html", {"request": request})
    return response

@router.get("/administrador/administradores/cadastrar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/cadastrar_administrador.html", {"request": request})
    return response

@router.get("/administrador/administradores/alterar/{id_administrador}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_administrador: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/alterar_administrador.html", {"request": request})
    return response

@router.get("/administrador/administradores/excluir/{id_administrador}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_administrador: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/excluir_administrador.html", {"request": request})
    return response

@router.get("/administrador/categorias_produtos")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/categorias_produtos.html", {"request": request})
    return response

@router.get("/administrador/categorias_produtos/cadastrar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/cadastrar_categoria_produto.html", {"request": request})
    return response

@router.get("/administrador/categorias_produtos/alterar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_categoria: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/alterar_categoria_produto.html", {"request": request})
    return response

@router.get("/administrador/categorias_produtos/excluir/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_categoria: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/excluir_categoria_produto.html", {"request": request})
    return response

@router.get("/administrador/categorias_servicos")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/categorias_servicos.html", {"request": request})
    return response

@router.get("/administrador/categorias_servicos/cadastrar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/cadastrar_categoria_servico.html", {"request": request})
    return response

@router.get("/administrador/categorias_servicos/alterar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_categoria: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/alterar_categoria_servico.html", {"request": request})
    return response

@router.get("/administrador/categorias_servicos/excluir/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_categoria: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/excluir_categoria_servico.html", {"request": request})
    return response

@router.get("/administrador/cadastros_pendentes")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/cadastros_pendentes.html", {"request": request})
    return response

@router.get("/administrador/validar_cadastro/{id_usuario}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, id_usuario: int, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/validar_cadastro.html", {"request": request})
    return response

@router.get("/administrador/usuarios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/usuarios.html", {"request": request})
    return response