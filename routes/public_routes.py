from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.usuario_model import TipoUsuario, Usuario
from model.profissional_model import Profissional
from repo import usuario_repo, profissional_repo
from util.auth_decorator import criar_sessao
from util.security import criar_hash_senha, verificar_senha
from util.usuario_util import usuario_para_sessao

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home(request: Request):
    response = templates.TemplateResponse("publico/home.html", {"request": request})
    return response


@router.get("/cadastro")
async def get_cadastro(request: Request):
    response = templates.TemplateResponse("publico/cadastro.html", {"request": request})
    return response


@router.get("/cadastro-noivos")
async def get_cadastro_noivos(request: Request):
    response = templates.TemplateResponse("publico/cadastro_noivos.html", {"request": request})
    return response


@router.post("/cadastro-noivos")
async def post_cadastro_noivos(request: Request,
    # Dados do primeiro noivo
    nome1: str = Form(...),
    data_nascimento1: str = Form(None),
    cpf1: str = Form(None),
    email1: str = Form(...),
    telefone1: str = Form(...),
    genero1: str = Form(None),
    # Dados do segundo noivo
    nome2: str = Form(...),
    data_nascimento2: str = Form(None),
    cpf2: str = Form(None),
    email2: str = Form(...),
    telefone2: str = Form(...),
    genero2: str = Form(None),
    # Dados de acesso compartilhados
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    # Dados do casamento
    data_casamento: str = Form(None),
    local_previsto: str = Form(None),
    orcamento: str = Form(None),
    numero_convidados: str = Form(None),
    newsletter: str = Form(None)
):
    # Verificar se as senhas coincidem
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": "As senhas não coincidem"}
        )

    # Verificar se emails já existem
    if usuario_repo.obter_usuario_por_email(email1):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": f"E-mail {email1} já cadastrado"}
        )

    if usuario_repo.obter_usuario_por_email(email2):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": f"E-mail {email2} já cadastrado"}
        )

    # Criar hash da senha compartilhada
    senha_hash = criar_hash_senha(senha)

    # Criar primeiro usuário
    usuario1 = Usuario(
        id=0,
        nome=nome1,
        cpf=cpf1,
        data_nascimento=data_nascimento1,
        email=email1,
        telefone=telefone1,
        senha=senha_hash,
        perfil=TipoUsuario.NOIVO,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )
    usuario1_id = usuario_repo.inserir_usuario(usuario1)

    # Criar segundo usuário
    usuario2 = Usuario(
        id=0,
        nome=nome2,
        cpf=cpf2,
        data_nascimento=data_nascimento2,
        email=email2,
        telefone=telefone2,
        senha=senha_hash,
        perfil=TipoUsuario.NOIVO,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )
    usuario2_id = usuario_repo.inserir_usuario(usuario2)

    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro-profissional")
async def get_cadastro_profissional(request: Request):
    response = templates.TemplateResponse("publico/cadastro_profissional.html", {"request": request})
    return response


@router.post("/cadastro-profissional")
async def post_cadastro_profissional(request: Request,
    nome: str = Form(...),
    data_nascimento: str = Form(None),
    cpf: str = Form(None),
    nome_empresa: str = Form(None),
    cnpj: str = Form(None),
    descricao: str = Form(None),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    perfis: list = Form(...),
    newsletter: str = Form(None)
):
    # Verificar se as senhas coincidem
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "publico/cadastro_profissional.html",
            {"request": request, "erro": "As senhas não coincidem"}
        )

    # Verificar se email já existe
    if usuario_repo.obter_usuario_por_email(email):
        return templates.TemplateResponse(
            "publico/cadastro_profissional.html",
            {"request": request, "erro": "E-mail já cadastrado"}
        )

    # Verificar se pelo menos um perfil foi selecionado
    if not perfis:
        return templates.TemplateResponse(
            "publico/cadastro_profissional.html",
            {"request": request, "erro": "Selecione pelo menos um tipo de profissional"}
        )

    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)

    # Verificar quais tipos de profissional foram selecionados
    eh_prestador = "PRESTADOR" in perfis
    eh_fornecedor = "FORNECEDOR" in perfis
    eh_locador = "LOCADOR" in perfis

    # Criar profissional (que herda de Usuario)
    profissional = Profissional(
        # Campos de Usuario na ordem correta
        id=0,
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        email=email,
        telefone=telefone,
        senha=senha_hash,
        perfil=TipoUsuario.PROFISSIONAL,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Profissional
        nome_empresa=nome_empresa,
        cnpj=cnpj,
        descricao=descricao,
        prestador=eh_prestador,
        fornecedor=eh_fornecedor,
        locador=eh_locador
    )
    profissional_id = profissional_repo.inserir_profissional(profissional)
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_geral")
async def get_cadastro_geral(request: Request):
    response = templates.TemplateResponse("publico/cadastro_fornecedor.html", {"request": request})
    return response


@router.post("/cadastro_geral")
async def post_cadastro_geral(request: Request,
    nome: str = Form(...),
    telefone: str = Form(None),
    email: str = Form(...),
    senha: str = Form(...),
    tipo: str = Form(...)
):
    # Verificar se email já existe
    if usuario_repo.obter_usuario_por_email(email):
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "E-mail já cadastrado"}
        )

    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)

    # Definir qual tipo de profissional baseado no tipo
    eh_prestador = tipo == "P"
    eh_fornecedor = tipo == "F"
    eh_locador = tipo == "L"

    # Criar profissional
    profissional = Profissional(
        # Campos de Usuario na ordem correta
        id=0,
        nome=nome,
        cpf=None,
        data_nascimento=None,
        email=email,
        telefone=telefone,
        senha=senha_hash,
        perfil=TipoUsuario.PROFISSIONAL,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Profissional
        nome_empresa=None,
        cnpj=None,
        descricao=None,
        prestador=eh_prestador,
        fornecedor=eh_fornecedor,
        locador=eh_locador
    )
    profissional_id = profissional_repo.inserir_profissional(profissional)
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_confirmacao")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_confirmacao.html", {"request": {}})
    return response

@router.get("/login")
async def get_login(request: Request):
    response = templates.TemplateResponse("publico/login.html", {"request": request})
    return response


@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = usuario_repo.obter_usuario_por_email(email)
    
    if not usuario or not verificar_senha(senha, usuario.senha):
       return templates.TemplateResponse(
    "publico/login.html",
    {"request": request, "erro": "Email ou senha inválidos"}
)


    
    # Criar sessão
    usuario_dict = usuario_para_sessao(usuario)
    criar_sessao(request, usuario_dict)
    
    # Redirecionar
    if redirect:
        return RedirectResponse(redirect, status.HTTP_303_SEE_OTHER)
    
    if usuario.perfil == TipoUsuario.ADMIN:
        return RedirectResponse("/administrador/dashboard", status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


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

