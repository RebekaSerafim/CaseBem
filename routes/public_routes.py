from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.fornecedor_model import Fornecedor
from model.usuario_model import TipoUsuario, Usuario
from repo import usuario_repo
from util.security import criar_hash_senha

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

@router.post("/cadastro/noivos")
async def post_root(request: Request,
    nome_noivo: str = Form(...),
    telefone_noivo: str = Form(None),
    email_noivo: str = Form(...),
    senha_noivo: str = Form(...),
    nome_noiva: str = Form(...),
    telefone_noiva: str = Form(None),
    email_noiva: str = Form(...),
    senha_noiva: str = Form(...)
):
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email_noivo):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "E-mail do noivo já cadastrado"}
        )
    if usuario_repo.obter_por_email(email_noiva):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "E-mail do noiva já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash_noivo = criar_hash_senha(senha_noivo)
    senha_hash_noiva = criar_hash_senha(senha_noiva)
    
    # Criar usuário
    usuario_noivo = Usuario(
        id=0,
        nome=nome_noivo,
        telefone=telefone_noivo,
        email=email_noivo,
        senha=senha_hash_noivo,
        perfil=TipoUsuario.NOIVO
    )
    usuario_noivo_id = usuario_repo.inserir(usuario_noivo)

    usuario_noiva = Usuario(
        id=0,
        nome=nome_noiva,
        telefone=telefone_noiva,
        email=email_noiva,
        senha=senha_hash_noiva,
        perfil=TipoUsuario.NOIVO
    )    
    usuario_noiva_id = usuario_repo.inserir(usuario_noiva)
    
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

@router.get("/cadastro/fornecedor")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_fornecedor.html", {"request": {}})
    return response

@router.post("/cadastro/fornecedor")
async def post_root(request: Request,
    nome: str = Form(...),
    telefone: str = Form(None),
    email: str = Form(...),
    senha: str = Form(...)
):
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "E-mail do noivo já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash_noivo = criar_hash_senha(senha)    
    
    # Criar usuário
    usuario_noivo = Fornecedor(
        id=0,
        nome=nome,
        telefone=telefone,
        email=email,
        senha=senha_hash_noivo,
        perfil=TipoUsuario.FORNECEDOR
    )
    usuario_noivo_id = usuario_repo.inserir(usuario_noivo)
    
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)

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

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

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

