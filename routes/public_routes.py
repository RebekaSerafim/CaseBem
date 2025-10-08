from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import Optional
import math

from core.models.usuario_model import TipoUsuario, Usuario
from core.models.fornecedor_model import Fornecedor
from core.models.casal_model import Casal
from dtos import CadastroNoivosDTO, CadastroFornecedorDTO
from core.repositories import usuario_repo, fornecedor_repo, casal_repo
from infrastructure.security import criar_sessao
from infrastructure.security import (
    criar_hash_senha,
    verificar_senha,
    validar_cnpj,
)
from util.usuario_util import usuario_para_sessao
from util.flash_messages import informar_sucesso
from util.template_helpers import template_response_with_flash, configurar_filtros_jinja
from util.error_handlers import tratar_erro_rota
from infrastructure.logging import logger
from util.pagination import PaginationHelper

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)


def get_active_page(request: Request) -> str:
    """Determina qual página está ativa baseada na URL"""
    url_path = str(request.url.path)

    if url_path == "/":
        return "home"
    elif url_path == "/sobre":
        return "sobre"
    elif url_path == "/contato":
        return "contato"
    elif url_path.startswith("/itens"):
        # Verificar parâmetros da query para determinar o tipo específico
        tipo_param = request.query_params.get("tipo")
        if tipo_param == "servico":
            return "servicos"
        elif tipo_param == "espaco":
            return "espacos"
        elif tipo_param == "produto":
            return "produtos"
        else:
            return "itens"
    elif url_path.startswith("/item/"):
        return "itens"
    else:
        return ""


def render_template_with_user(request: Request, template_name: str, context: dict = {}):
    """Renderiza template incluindo informações do usuário logado"""
    from infrastructure.security import obter_usuario_logado

    if context is None:
        context = {}

    context.update(
        {
            "request": request,
            "usuario_logado": obter_usuario_logado(request),
            "active_page": get_active_page(request),
        }
    )

    return templates.TemplateResponse(template_name, context)


@router.get("/")
@tratar_erro_rota(template_erro="publico/home.html")
async def get_home(request: Request, stay: Optional[str] = None):
    from infrastructure.security import obter_usuario_logado

    # Verificar se há usuário logado
    usuario_logado = obter_usuario_logado(request)

    # Se o parâmetro 'stay' não for fornecido e há usuário logado, redirecionar para dashboard
    if usuario_logado and not stay:
        # Redirecionar para o dashboard específico do usuário
        if usuario_logado.get("tipo") == "FORNECEDOR":
            return RedirectResponse(
                "/fornecedor/dashboard", status_code=status.HTTP_302_FOUND
            )
        elif usuario_logado.get("tipo") == "NOIVO":
            return RedirectResponse(
                "/noivo/dashboard", status_code=status.HTTP_302_FOUND
            )
        elif usuario_logado.get("tipo") == "ADMIN":
            return RedirectResponse(
                "/admin/dashboard", status_code=status.HTTP_302_FOUND
            )

    # Mostrar página inicial pública (com ou sem usuário logado)
    return render_template_with_user(request, "publico/home.html")


@router.get("/cadastro")
@tratar_erro_rota(template_erro="publico/cadastro.html")
async def get_cadastro(request: Request):
    return render_template_with_user(request, "publico/cadastro.html")


@router.get("/cadastro-noivos")
@tratar_erro_rota(template_erro="publico/cadastro_noivos.html")
async def get_cadastro_noivos(request: Request):
    return render_template_with_user(request, "publico/cadastro_noivos.html")


@router.post("/cadastro-noivos")
@tratar_erro_rota(template_erro="publico/cadastro_noivos.html")
async def post_cadastro_noivos(
    request: Request,
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
    newsletter: str = Form(None),
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
            newsletter=newsletter,
        )
    except ValidationError as e:
        # Extrair primeira mensagem de erro
        error_msg = e.errors()[0]["msg"]
        logger.warning(
            f"Erro de validação no cadastro de noivos: {error_msg}",
            email1=email1,
            email2=email2,
        )
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": error_msg, "dados": None},
        )

    # Validações adicionais usando UsuarioValidator
    from core.validators.usuario_validator import UsuarioValidator

    # Validar primeiro noivo
    valido, erro = UsuarioValidator.validar_dados_cadastro(
        nome=dados.nome1,
        email=dados.email1,
        senha=dados.senha,
        cpf=dados.cpf1,
        telefone=dados.telefone1
    )
    if not valido:
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": f"Primeiro noivo: {erro}", "dados": dados},
        )

    # Verificar email único do primeiro noivo
    valido, erro = UsuarioValidator.validar_email_unico(dados.email1)
    if not valido:
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": erro, "dados": dados},
        )

    # Validar segundo noivo
    valido, erro = UsuarioValidator.validar_dados_cadastro(
        nome=dados.nome2,
        email=dados.email2,
        senha=dados.senha,  # Mesma senha para ambos
        cpf=dados.cpf2,
        telefone=dados.telefone2
    )
    if not valido:
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": f"Segundo noivo: {erro}", "dados": dados},
        )

    # Verificar email único do segundo noivo
    valido, erro = UsuarioValidator.validar_email_unico(dados.email2)
    if not valido:
        return templates.TemplateResponse(
            "publico/cadastro_noivos.html",
            {"request": request, "erro": erro, "dados": dados},
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
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
    )
    usuario1_id = usuario_repo.inserir(usuario1)
    logger.info(
        f"Primeiro noivo cadastrado com sucesso",
        usuario_id=usuario1_id,
        email=dados.email1,
    )

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
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
    )
    usuario2_id = usuario_repo.inserir(usuario2)
    logger.info(
        f"Segundo noivo cadastrado com sucesso",
        usuario_id=usuario2_id,
        email=dados.email2,
    )

    # Criar registro do casal se ambos usuários foram criados com sucesso
    if usuario1_id and usuario2_id:
        casal = Casal(
            id=0,
            id_noivo1=usuario1_id,
            id_noivo2=usuario2_id,
            data_casamento=dados.data_casamento if dados.data_casamento else None,
            local_previsto=dados.local_previsto if dados.local_previsto else None,
            orcamento_estimado=(
                dados.orcamento_estimado if dados.orcamento_estimado else None
            ),
            numero_convidados=(
                int(dados.numero_convidados) if dados.numero_convidados else None
            ),
        )
        casal_id = casal_repo.inserir(casal)
        logger.info(
            f"Casal cadastrado com sucesso",
            casal_id=casal_id,
            noivo1_id=usuario1_id,
            noivo2_id=usuario2_id,
        )

    informar_sucesso(
        request, "Cadastro realizado com sucesso! Faça login para continuar."
    )
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro-fornecedor")
@tratar_erro_rota(template_erro="publico/cadastro_fornecedor.html")
async def get_cadastro_fornecedor(request: Request):
    response = templates.TemplateResponse(
        "publico/cadastro_fornecedor.html", {"request": request}
    )
    return response


@router.post("/cadastro-fornecedor")
@tratar_erro_rota(template_erro="publico/cadastro_fornecedor.html")
async def post_cadastro_fornecedor(
    request: Request,
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
    newsletter: str = Form(None),
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
            newsletter=newsletter,
        )
    except ValidationError as e:
        # Extrair primeira mensagem de erro
        error_msg = e.errors()[0]["msg"]
        logger.warning(
            f"Erro de validação no cadastro de fornecedor: {error_msg}",
            email=email,
            nome_empresa=nome_empresa,
        )
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": error_msg, "dados": None},
        )

    # Validações usando UsuarioValidator
    from core.validators.usuario_validator import UsuarioValidator

    # Validar dados do fornecedor
    valido, erro = UsuarioValidator.validar_dados_cadastro(
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha,
        cpf=dados.cpf,
        telefone=dados.telefone
    )
    if not valido:
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": erro, "dados": dados},
        )

    # Validar CNPJ se fornecido (lógica específica de fornecedor, não está no validator genérico)
    if dados.cnpj and not validar_cnpj(dados.cnpj):
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "CNPJ inválido", "dados": dados},
        )

    # Verificar email único
    valido, erro = UsuarioValidator.validar_email_unico(dados.email)
    if not valido:
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": erro, "dados": dados},
        )

    # Criar hash da senha
    senha_hash = criar_hash_senha(dados.senha)

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
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Fornecedor
        nome_empresa=dados.nome_empresa,
        cnpj=dados.cnpj,
        descricao=dados.descricao,
        newsletter=dados.newsletter == "on",
    )
    fornecedor_id = fornecedor_repo.inserir(fornecedor)
    logger.info(
        f"Fornecedor cadastrado com sucesso",
        fornecedor_id=fornecedor_id,
        email=dados.email,
        nome_empresa=dados.nome_empresa,
    )
    informar_sucesso(
        request, "Cadastro realizado com sucesso! Faça login para continuar."
    )
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_geral")
@tratar_erro_rota(template_erro="publico/cadastro_fornecedor.html")
async def get_cadastro_geral(request: Request):
    response = templates.TemplateResponse(
        "publico/cadastro_fornecedor.html", {"request": request}
    )
    return response


@router.post("/cadastro_geral")
@tratar_erro_rota(redirect_erro="/login")
async def post_cadastro_geral(
    request: Request,
    nome: str = Form(...),
    telefone: str = Form(None),
    email: str = Form(...),
    senha: str = Form(...),
    tipo: str = Form(...),
):
    # Verificar se email já existe
    if usuario_repo.obter_usuario_por_email(email):
        logger.warning(f"Tentativa de cadastro com email já existente", email=email)
        return templates.TemplateResponse(
            "publico/cadastro_fornecedor.html",
            {"request": request, "erro": "E-mail já cadastrado"},
        )

    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)

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
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None,
        # Campos específicos de Fornecedor
        nome_empresa=None,
        cnpj=None,
        descricao=None,
    )
    fornecedor_id = fornecedor_repo.inserir(fornecedor)
    logger.info(
        f"Cadastro geral realizado com sucesso",
        fornecedor_id=fornecedor_id,
        email=email,
        tipo=tipo,
    )
    return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro_confirmacao")
async def get_cadastro_confirmacao(request: Request):
    response = templates.TemplateResponse(
        "publico/cadastro_confirmacao.html", {"request": request}
    )
    return response


@router.get("/login")
@tratar_erro_rota(template_erro="publico/login.html")
async def get_login(request: Request, redirect: Optional[str] = None):
    context = {}
    if redirect:
        context["redirect"] = redirect
    return render_template_with_user(request, "publico/login.html", context)


@router.post("/login")
@tratar_erro_rota(template_erro="publico/login.html")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None),
):
    usuario = usuario_repo.obter_usuario_por_email(email)

    if not usuario or not verificar_senha(senha, usuario.senha):
        logger.warning(f"Tentativa de login falhou", email=email)
        return template_response_with_flash(
            templates,
            "publico/login.html",
            {"request": request, "erro": "Email ou senha inválidos"},
        )

    # Criar sessão
    usuario_dict = usuario_para_sessao(usuario)
    criar_sessao(request, usuario_dict)

    logger.info(
        f"Login realizado com sucesso",
        usuario_id=usuario.id,
        email=usuario.email,
        perfil=usuario.perfil.value,
    )

    # Adicionar mensagem de boas-vindas
    informar_sucesso(request, f"Bem-vindo, {usuario.nome}!")

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
@tratar_erro_rota(template_erro="publico/contato.html")
async def get_contato(request: Request):
    return render_template_with_user(request, "publico/contato.html")


@router.get("/sobre")
@tratar_erro_rota(template_erro="publico/sobre.html")
async def get_sobre(request: Request):
    return render_template_with_user(request, "publico/sobre.html")


@router.get("/itens")
@tratar_erro_rota(template_erro="publico/itens.html")
async def listar_itens_publicos(
    request: Request,
    tipo: Optional[str] = None,
    busca: Optional[str] = None,
    categoria: Optional[str] = None,
    pagina: int = 1,
):
    """Lista itens públicos com filtros e paginação"""
    from core.repositories import item_repo, categoria_repo
    from core.models.tipo_fornecimento_model import TipoFornecimento

    # Converter categoria para int se não estiver vazia
    categoria_int = None
    if categoria and categoria.strip():
        try:
            categoria_int = int(categoria)
        except ValueError:
            logger.warning(f"Categoria inválida fornecida", categoria=categoria)
            categoria_int = None

    # Obter categorias para o filtro
    categorias = []
    if tipo:
        tipo_map = {
            "produto": TipoFornecimento.PRODUTO,
            "servico": TipoFornecimento.SERVICO,
            "espaco": TipoFornecimento.ESPACO,
        }
        tipo_enum = tipo_map.get(tipo)
        if tipo_enum:
            categorias = categoria_repo.obter_ativas_por_tipo(tipo_enum)

    # Obter itens e total
    itens, total_itens = item_repo.obter_itens_publicos(
        tipo=tipo,
        busca=busca,
        categoria=categoria_int,
        pagina=pagina,
        tamanho_pagina=PaginationHelper.PUBLIC_PAGE_SIZE,
    )

    # Aplicar paginação
    page_info = PaginationHelper.paginate(
        itens,
        total_itens,
        pagina,
        PaginationHelper.PUBLIC_PAGE_SIZE
    )

    logger.info(
        f"Itens públicos listados",
        tipo=tipo,
        busca=busca,
        categoria=categoria_int,
        pagina=pagina,
        total_itens=total_itens,
    )

    return template_response_with_flash(
        templates,
        "publico/itens.html",
        {
            "request": request,
            "itens": page_info.items,
            "total_itens": page_info.total_items,
            "pagina_atual": page_info.current_page,
            "total_paginas": page_info.total_pages,
            "tipo": tipo,
            "busca": busca,
            "categoria": categoria_int,
            "categorias": categorias,
        },
    )


@router.get("/produtos")
async def produtos_redirect():
    """Redireciona para a página de itens com filtro de produtos"""
    return RedirectResponse("/itens?tipo=produto", status_code=status.HTTP_302_FOUND)


@router.get("/servicos")
async def servicos_redirect():
    """Redireciona para a página de itens com filtro de serviços"""
    return RedirectResponse("/itens?tipo=servico", status_code=status.HTTP_302_FOUND)


@router.get("/espacos")
async def espacos_redirect():
    """Redireciona para a página de itens com filtro de espaços"""
    return RedirectResponse("/itens?tipo=espaco", status_code=status.HTTP_302_FOUND)


@router.get("/locais")
async def locais_redirect():
    """Redireciona para a página de itens com filtro de espaços (alias para espacos)"""
    return RedirectResponse("/itens?tipo=espaco", status_code=status.HTTP_302_FOUND)


@router.get("/fornecedores")
async def get_fornecedores(request: Request):
    response = templates.TemplateResponse("publico/fornecedores.html", {"request": request})
    return response


@router.get("/prestadores")
async def get_prestadores(request: Request):
    response = templates.TemplateResponse("publico/prestadores.html", {"request": request})
    return response


@router.get("/locais/{id}")
async def get_local_detalhes(request: Request, id: int):
    response = templates.TemplateResponse(
        "publico/detalhes_local.html", {"request": request, "id": id}
    )
    return response


@router.get("/fornecedores/{id}")
async def get_fornecedor_detalhes(request: Request, id: int):
    response = templates.TemplateResponse(
        "publico/detalhes_fornecedor.html", {"request": request, "id": id}
    )
    return response


@router.get("/prestadores/{id}")
async def get_prestador_detalhes(request: Request, id: int):
    response = templates.TemplateResponse(
        "publico/detalhes_prestador.html", {"request": request, "id": id}
    )
    return response


@router.get("/item/{id}")
@tratar_erro_rota(template_erro="publico/item_detalhes.html")
async def detalhes_item_publico(request: Request, id: int):
    """Exibe detalhes de um item específico"""
    from core.repositories import item_repo

    item = item_repo.obter_item_publico_por_id(id)

    if not item:
        logger.warning(f"Item público não encontrado", item_id=id)
        return template_response_with_flash(
            templates,
            "publico/item_detalhes.html",
            {"request": request, "erro": "Item não encontrado"},
        )

    logger.info(f"Detalhes do item público exibidos", item_id=id, item_nome=item.get("nome", "desconhecido") if isinstance(item, dict) else item.nome)

    return template_response_with_flash(
        templates, "publico/item_detalhes.html", {"request": request, "item": item}
    )


@router.get("/produtos/{id}")
async def produto_detalhes_redirect(id: int):
    """Redireciona detalhes de produto para a nova rota unificada"""
    return RedirectResponse(
        f"/item/{id}", status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


@router.get("/servicos/{id}")
async def servico_detalhes_redirect(id: int):
    """Redireciona detalhes de serviço para a nova rota unificada"""
    return RedirectResponse(
        f"/item/{id}", status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


@router.get("/espacos/{id}")
async def espaco_detalhes_redirect(id: int):
    """Redireciona detalhes de espaço para a nova rota unificada"""
    return RedirectResponse(
        f"/item/{id}", status_code=status.HTTP_301_MOVED_PERMANENTLY
    )
