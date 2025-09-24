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
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso
from util.template_helpers import template_response_with_flash, configurar_filtros_jinja

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

def render_template_with_user(request: Request, template_name: str, context: dict = None):
    """Renderiza template incluindo informações do usuário logado"""
    from util.auth_decorator import obter_usuario_logado

    if context is None:
        context = {}

    context.update({
        "request": request,
        "usuario_logado": obter_usuario_logado(request),
        "active_page": get_active_page(request)
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

    informar_sucesso(request, "Cadastro realizado com sucesso! Faça login para continuar.")
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
        newsletter=dados.newsletter == "on"
    )
    fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)
    informar_sucesso(request, "Cadastro realizado com sucesso! Faça login para continuar.")
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
        descricao=None
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
       return template_response_with_flash(templates,
    "publico/login.html",
    {"request": request, "erro": "Email ou senha inválidos"}
)


    
    # Criar sessão
    usuario_dict = usuario_para_sessao(usuario)
    criar_sessao(request, usuario_dict)

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
async def get_contato(request: Request):
    return render_template_with_user(request, "publico/contato.html")

@router.get("/sobre")
async def get_sobre(request: Request):
    return render_template_with_user(request, "publico/sobre.html")

@router.get("/itens")
async def listar_itens_publicos(
    request: Request,
    tipo: str = None,
    busca: str = None,
    categoria: str = None,
    pagina: int = 1
):
    """Lista itens públicos com filtros e paginação"""
    try:
        from repo import item_repo, categoria_repo
        from model.item_model import TipoItem
        import math

        # Converter categoria para int se não estiver vazia
        categoria_int = None
        if categoria and categoria.strip():
            try:
                categoria_int = int(categoria)
            except ValueError:
                categoria_int = None

        # Obter categorias para o filtro
        categorias = []
        if tipo:
            tipo_map = {
                'produto': TipoItem.PRODUTO,
                'servico': TipoItem.SERVICO,
                'espaco': TipoItem.ESPACO
            }
            tipo_enum = tipo_map.get(tipo)
            if tipo_enum:
                categorias = categoria_repo.obter_categorias_por_tipo_ativas(tipo_enum)

        # Obter itens e total
        itens, total_itens = item_repo.obter_itens_publicos(
            tipo=tipo,
            busca=busca,
            categoria=categoria_int,
            pagina=pagina,
            tamanho_pagina=12
        )

        # Calcular total de páginas
        total_paginas = math.ceil(total_itens / 12) if total_itens > 0 else 1

        return template_response_with_flash(templates, "publico/itens.html", {
            "request": request,
            "itens": itens,
            "total_itens": total_itens,
            "pagina_atual": pagina,
            "total_paginas": total_paginas,
            "tipo": tipo,
            "busca": busca,
            "categoria": categoria_int,
            "categorias": categorias
        })

    except Exception as e:
        print(f"Erro ao listar itens públicos: {e}")
        return template_response_with_flash(templates, "publico/itens.html", {
            "request": request,
            "itens": [],
            "total_itens": 0,
            "pagina_atual": 1,
            "total_paginas": 1,
            "tipo": tipo,
            "busca": busca,
            "erro": "Erro ao carregar itens"
        })

@router.get("/produtos")
async def produtos_redirect(request: Request):
    """Redireciona para a página de itens com filtro de produtos"""
    return RedirectResponse("/itens?tipo=produto", status_code=status.HTTP_302_FOUND)

@router.get("/servicos")
async def servicos_redirect(request: Request):
    """Redireciona para a página de itens com filtro de serviços"""
    return RedirectResponse("/itens?tipo=servico", status_code=status.HTTP_302_FOUND)

@router.get("/espacos")
async def espacos_redirect(request: Request):
    """Redireciona para a página de itens com filtro de espaços"""
    return RedirectResponse("/itens?tipo=espaco", status_code=status.HTTP_302_FOUND)

@router.get("/locais")
async def locais_redirect(request: Request):
    """Redireciona para a página de itens com filtro de espaços (alias para espacos)"""
    return RedirectResponse("/itens?tipo=espaco", status_code=status.HTTP_302_FOUND)

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

@router.get("/item/{id}")
async def detalhes_item_publico(request: Request, id: int):
    """Exibe detalhes de um item específico"""
    try:
        from repo import item_repo

        item = item_repo.obter_item_publico_por_id(id)

        if not item:
            return template_response_with_flash(templates, "publico/item_detalhes.html", {
                "request": request,
                "erro": "Item não encontrado"
            })

        return template_response_with_flash(templates, "publico/item_detalhes.html", {
            "request": request,
            "item": item
        })

    except Exception as e:
        print(f"Erro ao obter detalhes do item: {e}")
        return template_response_with_flash(templates, "publico/item_detalhes.html", {
            "request": request,
            "erro": "Erro ao carregar detalhes do item"
        })

@router.get("/produtos/{id}")
async def produto_detalhes_redirect(id: int):
    """Redireciona detalhes de produto para a nova rota unificada"""
    return RedirectResponse(f"/item/{id}", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/servicos/{id}")
async def servico_detalhes_redirect(id: int):
    """Redireciona detalhes de serviço para a nova rota unificada"""
    return RedirectResponse(f"/item/{id}", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.get("/espacos/{id}")
async def espaco_detalhes_redirect(id: int):
    """Redireciona detalhes de espaço para a nova rota unificada"""
    return RedirectResponse(f"/item/{id}", status_code=status.HTTP_301_MOVED_PERMANENTLY)


