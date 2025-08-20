from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/fornecedor/dashboard")
async def get_root():
    response = templates.TemplateResponse("fornecedor/dashboard.html", {"request": {}})
    return response

@router.get("/fornecedor/cadastar_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/cadastrar_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/alterar_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/alterar_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/excluir_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/excluir_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/detalhes_do_produto")
async def get_root():
    response = templates.TemplateResponse("fornecedor/detalhes_do_produto.html", {"request": {}})
    return response

@router.get("/fornecedor/dados_do_perfil")
async def get_root():
    response = templates.TemplateResponse("fornecedor/dados_do_perfil.html", {"request": {}})
    return response




