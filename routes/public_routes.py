from fastapi import APIRouter, Form, Request, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
import os

from model.usuario_model import TipoUsuario, Usuario
from model.fornecedor_model import Fornecedor
from model.casal_model import Casal
from dtos.cadastro_noivos_dto import CadastroNoivosDTO
from dtos.cadastro_fornecedor_dto import CadastroFornecedorDTO
from repo import usuario_repo, fornecedor_repo, casal_repo
from util.auth_decorator import criar_sessao
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha, validar_cpf, validar_cnpj, validar_telefone
from util.usuario_util import usuario_para_sessao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def render_template_with_user(request: Request, template_name: str, context: dict = None):
    """Renderiza template incluindo informações do usuário logado"""
    from util.auth_decorator import obter_usuario_logado

    if context is None:
        context = {}

    context.update({
        "request": request,
        "usuario_logado": obter_usuario_logado(request)
    })

    return templates.TemplateResponse(template_name, context)



@router.get("/")
async def get_home(request: Request, stay: str = None):
    from util.auth_decorator import obter_usuario_logado

    # Verificar se há usuário logado
    usuario_logado = obter_usuario_logado(request)

    # Se o parâmetro 'stay' não for fornecido e há usuário logado, redirecionar para dashboard
    if usuario_logado and not stay:
        # Redirecionar para o dashboard específico do usuário
        if usuario_logado.get("tipo") == "FORNECEDOR":
            return RedirectResponse("/fornecedor/dashboard", status_code=status.HTTP_302_FOUND)
        elif usuario_logado.get("tipo") == "NOIVO":
            return RedirectResponse("/noivo/dashboard", status_code=status.HTTP_302_FOUND)
        elif usuario_logado.get("tipo") == "ADMIN":
            return RedirectResponse("/admin/dashboard", status_code=status.HTTP_302_FOUND)

    # Mostrar página inicial pública (com ou sem usuário logado)
    return render_template_with_user(request, "publico/home.html")


@router.get("/cadastro")
async def get_cadastro(request: Request):
    return render_template_with_user(request, "publico/cadastro.html")


@router.get("/cadastro-noivos")
async def get_cadastro_noivos(request: Request):
    return render_template_with_user(request, "publico/cadastro_noivos.html")


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
    try:
        # Criar DTO com validação automática do Pydantic
        dados = CadastroNoivosDTO(
            # Dados do casamento
            data_casamento=data_casamento,
            local_previsto=local_previsto,
            orcamento_estimado=orcamento,
            numero_convidados=numero_convidados,
            # Dados do primeiro noivo
            nome1=nome1,
            data_nascimento1=data_nascimento1,
            cpf1=cpf1,
            email1=email1,
            telefone1=telefone1,
            genero1=genero1,
            # Dados do segundo noivo
            nome2=nome2,
            data_nascimento2=data_nascimento2,
            cpf2=cpf2,
            email2=email2,
            telefone2=telefone2,
            genero2=genero2,
            # Dados de acesso
            senha=senha,
            confirmar_senha=confirmar_senha,
            # Outros
            newsletter=newsletter
        )
    except ValidationError as e:
        # Extrair primeira mensagem de erro
        error_msg = e.errors()[0]['msg']
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": error_msg, "dados": None}
        )

    # Validações adicionais específicas do negócio
    # Validar força da senha
    senha_valida, erro_senha = validar_forca_senha(dados.senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": erro_senha, "dados": dados}
        )

    # Validar CPFs se fornecidos
    if dados.cpf1 and not validar_cpf(dados.cpf1):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": "CPF do primeiro noivo é inválido", "dados": dados}
        )

    if dados.cpf2 and not validar_cpf(dados.cpf2):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": "CPF do segundo noivo é inválido", "dados": dados}
        )

    # Validar telefones
    if not validar_telefone(dados.telefone1):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": "Telefone do primeiro noivo é inválido", "dados": dados}
        )

    if not validar_telefone(dados.telefone2):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": "Telefone do segundo noivo é inválido", "dados": dados}
        )

    # Verificar se emails já existem
    if usuario_repo.obter_usuario_por_email(dados.email1):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": f"E-mail {dados.email1} já cadastrado", "dados": dados}
        )

    if usuario_repo.obter_usuario_por_email(dados.email2):
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": f"E-mail {dados.email2} já cadastrado", "dados": dados}
        )

    # Criar hash da senha compartilhada
    senha_hash = criar_hash_senha(dados.senha)

    # Criar primeiro usuário
    usuario1 = Usuario(
        id=0,
        nome=dados.nome1,
        cpf=dados.cpf1,
        data_nascimento=dados.data_nascimento1,
        email=dados.email1,
        telefone=dados.telefone1,
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
        nome=dados.nome2,
        cpf=dados.cpf2,
        data_nascimento=dados.data_nascimento2,
        email=dados.email2,
        telefone=dados.telefone2,
        senha=senha_hash,
        perfil=TipoUsuario.NOIVO,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )
    usuario2_id = usuario_repo.inserir_usuario(usuario2)

    # Criar registro do casal se ambos usuários foram criados com sucesso
    if usuario1_id and usuario2_id:
        casal = Casal(
            id=0,
            id_noivo1=usuario1_id,
            id_noivo2=usuario2_id,
            data_casamento=dados.data_casamento if dados.data_casamento else None,
            local_previsto=dados.local_previsto if dados.local_previsto else None,
            orcamento_estimado=dados.orcamento_estimado if dados.orcamento_estimado else None,
            numero_convidados=int(dados.numero_convidados) if dados.numero_convidados else None
        )
        casal_repo.inserir_casal(casal)

    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro-fornecedor")
async def get_cadastro_fornecedor(request: Request):
    response = templates.TemplateResponse("publico/cadastro_fornecedor.html", {"request": request})
    return response


@router.post("/cadastro-fornecedor")
async def post_cadastro_fornecedor(request: Request,
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
    try:
        # Criar DTO com validação automática do Pydantic
        dados = CadastroFornecedorDTO(
            nome=nome,
            data_nascimento=data_nascimento,
            cpf=cpf,
            nome_empresa=nome_empresa,
            cnpj=cnpj,
            descricao=descricao,
            email=email,
            telefone=telefone,
            senha=senha,
            confirmar_senha=confirmar_senha,
            perfis=perfis if perfis else [],
            newsletter=newsletter
        )
    except ValidationError as e:
        # Extrair primeira mensagem de erro
        error_msg = e.errors()[0]['msg']
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": error_msg, "dados": None}
        )

    # Validações adicionais específicas do negócio
    # Validar força da senha
    senha_valida, erro_senha = validar_forca_senha(dados.senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": erro_senha, "dados": dados}
        )

    # Validar CPF se fornecido
    if dados.cpf and not validar_cpf(dados.cpf):
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "CPF inválido", "dados": dados}
        )

    # Validar CNPJ se fornecido
    if dados.cnpj and not validar_cnpj(dados.cnpj):
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "CNPJ inválido", "dados": dados}
        )

    # Validar telefone
    if not validar_telefone(dados.telefone):
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "Telefone inválido", "dados": dados}
        )

    # Verificar se email já existe
    if usuario_repo.obter_usuario_por_email(dados.email):
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "E-mail já cadastrado", "dados": dados}
        )

    # Criar hash da senha
    senha_hash = criar_hash_senha(dados.senha)

    # Verificar quais tipos de fornecimento foram selecionados
    eh_prestador = "prestador" in dados.perfis
    eh_vendedor = "vendedor" in dados.perfis
    eh_locador = "locador" in dados.perfis

    # Criar fornecedor (que herda de Usuario)
    fornecedor = Fornecedor(
        # Campos de Usuario na ordem correta
        id=0,
        nome=dados.nome,
        cpf=dados.cpf,
        data_nascimento=dados.data_nascimento,
        email=dados.email,
        telefone=dados.telefone,
        senha=senha_hash,
        perfil=TipoUsuario.FORNECEDOR,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Fornecedor
        nome_empresa=dados.nome_empresa,
        cnpj=dados.cnpj,
        descricao=dados.descricao,
        prestador=eh_prestador,
        vendedor=eh_vendedor,
        locador=eh_locador,
        newsletter=dados.newsletter == "on"
    )
    fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)
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

    # Definir qual tipo de fornecedor baseado no tipo
    eh_prestador = tipo == "P"
    eh_vendedor = tipo == "F"
    eh_locador = tipo == "L"

    # Criar fornecedor
    fornecedor = Fornecedor(
        # Campos de Usuario na ordem correta
        id=0,
        nome=nome,
        cpf=None,
        data_nascimento=None,
        email=email,
        telefone=telefone,
        senha=senha_hash,
        perfil=TipoUsuario.FORNECEDOR,
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Fornecedor
        nome_empresa=None,
        cnpj=None,
        descricao=None,
        prestador=eh_prestador,
        vendedor=eh_vendedor,
        locador=eh_locador
    )
    fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_confirmacao")
async def get_root():
    response = templates.TemplateResponse("publico/cadastro_confirmacao.html", {"request": {}})
    return response

@router.get("/login")
async def get_login(request: Request):
    return render_template_with_user(request, "publico/login.html")


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
        return RedirectResponse("/admin/dashboard", status.HTTP_303_SEE_OTHER)
    elif usuario.perfil == TipoUsuario.FORNECEDOR:
        return RedirectResponse("/fornecedor/dashboard", status.HTTP_303_SEE_OTHER)
    elif usuario.perfil == TipoUsuario.NOIVO:
        return RedirectResponse("/noivo/dashboard", status.HTTP_303_SEE_OTHER)
    
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


