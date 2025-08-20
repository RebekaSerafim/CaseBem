from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/administrador/dashboard")
async def get_root():
    response = templates.TemplateResponse("administrador/dashboard.html", {"request": {}})
    return response

@router.get("/administrador/administradores")
async def get_root():
    response = templates.TemplateResponse("administrador/administradores.html", {"request": {}})
    return response

@router.get("/administrador/administradores/cadastrar")
async def get_root():
    response = templates.TemplateResponse("administrador/cadastrar_administrador.html", {"request": {}})
    return response

@router.get("/administrador/administradores/alterar/{id_administrador}")
async def get_root(id_administrador: int):
    response = templates.TemplateResponse("administrador/alterar_administrador.html", {"request": {}})
    return response

@router.get("/administrador/administradores/excluir/{id_administrador}")
async def get_root(id_administrador: int):
    response = templates.TemplateResponse("administrador/excluir_administrador.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos")
async def get_root():
    response = templates.TemplateResponse("administrador/categorias_produtos.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos/cadastrar")
async def get_root():
    response = templates.TemplateResponse("administrador/cadastrar_categoria_produto.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos/alterar/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/alterar_categoria_produto.html", {"request": {}})
    return response

@router.get("/administrador/categorias_produtos/excluir/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/excluir_categoria_produto.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos")
async def get_root():
    response = templates.TemplateResponse("administrador/categorias_servicos.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos/cadastrar")
async def get_root():    
    response = templates.TemplateResponse("administrador/cadastrar_categoria_servico.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos/alterar/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/alterar_categoria_servico.html", {"request": {}})
    return response

@router.get("/administrador/categorias_servicos/excluir/{id_categoria}")
async def get_root(id_categoria: int):
    response = templates.TemplateResponse("administrador/excluir_categoria_servico.html", {"request": {}})
    return response

@router.get("/administrador/cadastros_pendentes")
async def get_root():
    response = templates.TemplateResponse("administrador/cadastros_pendentes.html", {"request": {}})
    return response

@router.get("/administrador/validar_cadastro/{id_usuario}")
async def get_root(id_usuario: int):
    response = templates.TemplateResponse("administrador/validar_cadastro.html", {"request": {}})
    return response

@router.get("/administrador/usuarios")
async def get_root():
    response = templates.TemplateResponse("administrador/usuarios.html", {"request": {}})
    return response