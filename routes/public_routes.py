from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root():
    response = templates.TemplateResponse("publico/home.html", {"request": {}})
    return response

@router.get("/cadastro")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro.html", {"request": {}})
    return response

@router.get("/cadastro/noivos")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_noivos.html", {"request": {}})
    return response

@router.get("/cadastro/fornecedor")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_fornecedor.html", {"request": {}})
    return response

@router.get("/cadastro/prestador")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_prestador.html", {"request": {}})
    return response

@router.get("/cadastro/locador")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_locador.html", {"request": {}})
    return response

@router.get("/cadastro/confirmacao")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_confirmacao.html", {"request": {}})
    return response

@router.get("/login")
async def get_root():
    response = templates.TemplateResponse("publico/login.html", {"request": {}})
    return response

@router.get("/contato")
async def get_root():
    response = templates.TemplateResponse("publico/contato.html", {"request": {}})
    return response

@router.get("/sobre")
async def get_root():
    response = templates.TemplateResponse("publico/sobre.html", {"request": {}})
    return response

@router.get("/produtos")
async def get_root():
    response = templates.TemplateResponse("publico/produtos.html", {"request": {}})
    return response

@router.get("/servicos")
async def get_root():
    response = templates.TemplateResponse("publico/servicos.html", {"request": {}})
    return response

@router.get("/locais")
async def get_root():
    response = templates.TemplateResponse("publico/locais.html", {"request": {}})
    return response

@router.get("/fornecedores")
async def get_root():
    response = templates.TemplateResponse("publico/fornecedores.html", {"request": {}})
    return response

@router.get("/prestadores")
async def get_root():
    response = templates.TemplateResponse("publico/prestadores.html", {"request": {}})
    return response

@router.get("/locais/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_local.html", {"request": {}, "id": id})
    return response

@router.get("/fornecedores/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_fornecedor.html", {"request": {}, "id": id})
    return response

@router.get("/prestadores/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_prestador.html", {"request": {}, "id": id})
    return response

@router.get("/produtos/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_produto.html", {"request": {}, "id": id})
    return response

@router.get("/servicos/{id}")
async def get_root(id: int):
    response = templates.TemplateResponse("publico/detalhes_servico.html", {"request": {}, "id": id})
    return response

