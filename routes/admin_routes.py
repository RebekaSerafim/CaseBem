from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from infrastructure.security import requer_autenticacao
from util.error_handlers import tratar_erro_rota
from util.exceptions import ValidacaoError
from infrastructure.logging import logger
from core.models.usuario_model import TipoUsuario
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories import usuario_repo, fornecedor_repo, item_repo, categoria_repo, orcamento_repo, demanda_repo
from util.flash_messages import informar_sucesso, informar_erro
from util.template_helpers import configurar_filtros_jinja

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

# Importar função centralizada de route_helpers
from util.route_helpers import get_active_page

def get_admin_active_page(request: Request) -> str:
    """
    Determina qual página está ativa na área admin.
    DEPRECATED: Usa get_active_page do route_helpers.
    Mantido para compatibilidade.
    """
    return get_active_page(request, "admin")

def render_admin_template(request: Request, template_name: str, context: dict = {}):
    """Renderiza template admin incluindo active_page"""  
    context.update({
        "active_page": get_admin_active_page(request)
    })

    return templates.TemplateResponse(template_name, context)

# ==================== REDIRECIONAMENTO RAIZ ====================

@router.get("/admin")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def admin_root(request: Request, usuario_logado: dict = {}):
    """Redireciona /admin para /admin/dashboard"""
    return RedirectResponse("/admin/dashboard", status_code=status.HTTP_302_FOUND)

# ==================== PERFIL ADMIN ====================

@router.get("/admin/perfil")
@requer_autenticacao([TipoUsuario.ADMIN.value])
@tratar_erro_rota(template_erro="admin/perfil.html")
async def perfil_admin(request: Request, usuario_logado: dict = {}):
    """Página de perfil do administrador"""
    admin = usuario_repo.obter_por_id(usuario_logado['id'])
    logger.info("Perfil do admin carregado com sucesso", admin_id=usuario_logado['id'])

    return templates.TemplateResponse("admin/perfil.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "admin": admin,
        "active_page": get_admin_active_page(request)
    })

@router.post("/admin/perfil")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def atualizar_perfil_admin(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(""),
    cargo: str = Form(""),
    endereco: str = Form(""),
    cidade: str = Form(""),
    estado: str = Form(""),
    observacoes: str = Form(""),
    usuario_logado: dict = {}
):
    """Atualiza o perfil do administrador"""
    try:
        admin = usuario_repo.obter_por_id(usuario_logado['id'])
        if not admin:
            return templates.TemplateResponse("admin/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Atualizar dados do usuário
        admin.nome = nome
        admin.email = email
        admin.telefone = telefone if telefone else None

        # Campos específicos do admin podem ser armazenados como propriedades customizadas
        # ou em uma tabela separada dependendo da implementação do banco

        sucesso = usuario_repo.atualizar(admin)

        if sucesso:
            # Atualizar a sessão com os novos dados
            usuario_logado['nome'] = nome
            usuario_logado['email'] = email

            return templates.TemplateResponse("admin/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "sucesso": "Perfil atualizado com sucesso!"
            })
        else:
            return templates.TemplateResponse("admin/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "erro": "Erro ao atualizar perfil"
            })

    except Exception as e:
        logger.error("Erro ao atualizar perfil admin: ", erro=e)
        admin = usuario_repo.obter_por_id(usuario_logado['id'])
        return templates.TemplateResponse("admin/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
            "erro": "Erro ao atualizar perfil"
        })

# ==================== DASHBOARD ====================

@router.get("/admin/dashboard")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def dashboard_admin(request: Request, usuario_logado: dict = {}):
    """Dashboard principal do administrador"""
    try:
        # Estatísticas do sistema
        stats = {
            "total_usuarios": usuario_repo.contar(),
            "total_fornecedores": fornecedor_repo.contar(),
            "total_noivos": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.NOIVO),
            "total_admins": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.ADMIN),
            "fornecedores_nao_verificados": fornecedor_repo.contar_nao_verificados(),
            "total_itens": item_repo.contar(),
            "total_categorias": categoria_repo.contar(),
            "total_orcamentos": orcamento_repo.contar(),
            "total_demandas": demanda_repo.contar(),
            "estatisticas_itens": {
                "produtos": item_repo.contar_itens_por_tipo(TipoFornecimento.PRODUTO),
                "servicos": item_repo.contar_itens_por_tipo(TipoFornecimento.SERVICO),
                "espacos": item_repo.contar_itens_por_tipo(TipoFornecimento.ESPACO)
            }
        }

        # Buscar fornecedores recentes
        fornecedores_recentes = fornecedor_repo.obter_fornecedores_por_pagina(1, 5)

        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats": stats,
            "fornecedores_recentes": fornecedores_recentes,
            "active_page": get_admin_active_page(request)
        })
    except Exception as e:
        logger.error("Erro no dashboard admin: ", erro=e)
        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar estatísticas",
            "active_page": get_admin_active_page(request)
        })

# ==================== GESTÃO DE USUÁRIOS ====================

@router.get("/admin/usuarios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_usuarios(
    request: Request,
    pagina: int = 1,
    usuario_logado: dict = {}
):
    """Lista todos os usuários do sistema com filtros e paginação"""
    try:
        import math

        # Obter parâmetros de filtro da URL
        busca = request.query_params.get("search", "").strip()
        tipo_usuario = request.query_params.get("tipo_usuario", "").strip()
        status = request.query_params.get("status", "").strip()
        tamanho_pagina = 10

        # Aplicar filtros se fornecidos, senão listar todos
        if busca or tipo_usuario or status:
            usuarios, total_usuarios = usuario_repo.buscar_usuarios_paginado(
                busca=busca,
                tipo_usuario=tipo_usuario,
                status=status,
                pagina=pagina,
                tamanho_pagina=tamanho_pagina
            )
        else:
            usuarios, total_usuarios = usuario_repo.obter_usuarios_paginado(
                pagina=pagina,
                tamanho_pagina=tamanho_pagina
            )

        # Calcular total de páginas
        total_paginas = math.ceil(total_usuarios / tamanho_pagina) if total_usuarios > 0 else 1

        # Buscar dados de fornecedores para verificar status de verificação
        fornecedores_dados = {}
        for usuario in usuarios:
            if usuario.perfil == TipoUsuario.FORNECEDOR:
                fornecedor = fornecedor_repo.obter_por_id(usuario.id)
                if fornecedor:
                    fornecedores_dados[usuario.id] = fornecedor

        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "usuarios": usuarios,
            "fornecedores_dados": fornecedores_dados,
            "total_usuarios": total_usuarios,
            "pagina_atual": pagina,
            "total_paginas": total_paginas,
            "busca": busca,
            "tipo_usuario": tipo_usuario,
            "status": status
        })
    except Exception as e:
        logger.error("Erro ao listar usuários: ", erro=e)
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar usuários",
            "usuarios": [],
            "total_usuarios": 0,
            "pagina_atual": 1,
            "total_paginas": 1
        })

# ==================== GESTÃO DE ADMINISTRADORES ====================

@router.get("/admin/usuarios/novo-admin")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def novo_admin_form(request: Request, usuario_logado: dict = {}):
    """Formulário para cadastrar novo administrador"""
    return templates.TemplateResponse("admin/admin_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar"
    })

@router.post("/admin/usuarios/criar-admin")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def criar_admin(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(""),
    telefone: str = Form(""),
    data_nascimento: str = Form(""),
    senha: str = Form(...),
    usuario_logado: dict = {}
):
    """Cria um novo administrador"""
    try:
        # Validar se o nome não está vazio
        nome = nome.strip()
        if not nome:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Nome é obrigatório"
            })

        # Validar se o email não está vazio
        email = email.strip()
        if not email:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Email é obrigatório"
            })

        # Verificar se já existe usuário com o mesmo email
        usuario_existente = usuario_repo.obter_usuario_por_email(email)
        if usuario_existente:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": f"Já existe um usuário cadastrado com o email {email}"
            })

        # Validar senha
        if not senha or len(senha) < 6:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Senha deve ter pelo menos 6 caracteres"
            })

        # Limpar campos opcionais
        from typing import Optional
        cpf_limpo: Optional[str] = cpf.strip() if cpf and cpf.strip() else None
        telefone_limpo: str = telefone.strip() if telefone and telefone.strip() else ""
        data_nascimento_limpo: Optional[str] = data_nascimento.strip() if data_nascimento and data_nascimento.strip() else None

        # Hash da senha
        from infrastructure.security import criar_hash_senha
        senha_hash = criar_hash_senha(senha)

        # Criar objeto Usuario
        from core.models.usuario_model import Usuario
        novo_admin = Usuario(
            id=0,
            nome=nome,
            cpf=cpf_limpo,
            data_nascimento=data_nascimento_limpo,
            email=email,
            telefone=telefone_limpo,
            senha=senha_hash,
            perfil=TipoUsuario.ADMIN,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            ativo=True
        )

        # Inserir no banco
        admin_id = usuario_repo.inserir(novo_admin)
        if admin_id:
            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "acao": "criar",
                "erro": "Erro ao cadastrar administrador"
            })

    except Exception as e:
        logger.error("Erro ao criar administrador: ", erro=e)
        return templates.TemplateResponse("admin/admin_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "criar",
            "erro": "Erro interno do servidor"
        })

@router.get("/admin/usuarios/editar-admin/{id_admin}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def editar_admin_form(request: Request, id_admin: int, usuario_logado: dict = {}):
    """Formulário para editar administrador"""
    try:
        admin = usuario_repo.obter_por_id(id_admin)
        if not admin or admin.perfil != TipoUsuario.ADMIN:
            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("admin/admin_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
            "acao": "editar"
        })
    except Exception as e:
        logger.error("Erro ao carregar administrador para edição: ", erro=e)
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/usuarios/atualizar-admin/{id_admin}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def atualizar_admin(
    request: Request,
    id_admin: int,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(""),
    telefone: str = Form(""),
    data_nascimento: str = Form(""),
    usuario_logado: dict = {}
):
    """Atualiza dados do administrador"""
    try:
        # Obter administrador atual
        admin = usuario_repo.obter_por_id(id_admin)
        if not admin or admin.perfil != TipoUsuario.ADMIN:
            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

        # Validar campos obrigatórios
        nome = nome.strip()
        email = email.strip()

        if not nome:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": "Nome é obrigatório"
            })

        if not email:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": "Email é obrigatório"
            })

        # Verificar se email já existe (exceto para o próprio usuário)
        usuario_existente = usuario_repo.obter_usuario_por_email(email)
        if usuario_existente and usuario_existente.id != id_admin:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": f"Já existe outro usuário cadastrado com o email {email}"
            })

        # Atualizar dados
        admin.nome = nome
        admin.email = email
        admin.cpf = cpf.strip() if cpf.strip() else None
        admin.telefone = telefone.strip() if telefone.strip() else None
        admin.data_nascimento = data_nascimento.strip() if data_nascimento.strip() else None

        if usuario_repo.atualizar(admin):
            # Atualizar sessão se o admin editou a si mesmo
            if usuario_logado['id'] == id_admin:
                usuario_logado['nome'] = nome
                usuario_logado['email'] = email

            return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/admin_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "admin": admin,
                "acao": "editar",
                "erro": "Erro ao atualizar administrador"
            })

    except Exception as e:
        logger.error("Erro ao atualizar administrador: ", erro=e)
        admin = usuario_repo.obter_por_id(id_admin)
        return templates.TemplateResponse("admin/admin_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "admin": admin,
            "acao": "editar",
            "erro": "Erro interno do servidor"
        })

@router.get("/admin/usuarios/{id_usuario}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def visualizar_usuario(request: Request, id_usuario: int, usuario_logado: dict = {}):
    """Visualiza detalhes de um usuário específico"""
    try:
        usuario = usuario_repo.obter_por_id(id_usuario)

        if not usuario:
            return templates.TemplateResponse("admin/usuarios.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Se for fornecedor, buscar dados adicionais
        fornecedor = None
        if usuario.perfil == TipoUsuario.FORNECEDOR:
            fornecedor = fornecedor_repo.obter_por_id(id_usuario)

        return templates.TemplateResponse("admin/usuario_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "usuario": usuario,
            "fornecedor": fornecedor
        })
    except Exception as e:
        logger.error("Erro ao visualizar usuário: ", erro=e)
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar usuário"
        })

@router.post("/admin/usuarios/{id_usuario}/bloquear")
@requer_autenticacao([TipoUsuario.ADMIN.value])
@tratar_erro_rota(redirect_erro="/admin/usuarios")
async def bloquear_usuario(request: Request, id_usuario: int, usuario_logado: dict = {}):
    """Bloqueia um usuário"""
    if id_usuario <= 0:
        raise ValidacaoError("ID do usuário deve ser um número positivo", "id_usuario", id_usuario)

    sucesso = usuario_repo.bloquear_usuario(id_usuario)
    if sucesso:
        logger.info("Usuário bloqueado com sucesso", id_usuario=id_usuario, admin_id=usuario_logado['id'])
        informar_sucesso(request, "Usuário bloqueado com sucesso!")
    else:
        logger.warning("Falha ao bloquear usuário", id_usuario=id_usuario)
        informar_erro(request, "Erro ao bloquear usuário!")

    return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/usuarios/{id_usuario}/ativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def ativar_usuario(request: Request, id_usuario: int, usuario_logado: dict = {}):
    """Ativa um usuário"""
    try:
        sucesso = usuario_repo.ativar_usuario(id_usuario)
        if sucesso:
            informar_sucesso(request, "Usuário ativado com sucesso!")
        else:
            informar_erro(request, "Erro ao ativar usuário!")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error("Erro ao ativar usuário: ", erro=e)
        informar_erro(request, "Erro ao ativar usuário!")
        return RedirectResponse("/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)


# ==================== VERIFICAÇÃO DE FORNECEDORES ====================

@router.get("/admin/verificacao/{id_fornecedor}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def verificacao_fornecedor_especifico(request: Request, id_fornecedor: int, usuario_logado: dict = {}):
    """Página de verificação para um fornecedor específico"""
    try:
        # Buscar o usuário e dados do fornecedor
        usuario = usuario_repo.obter_por_id(id_fornecedor)
        if not usuario or usuario.perfil != TipoUsuario.FORNECEDOR:
            return templates.TemplateResponse("admin/verificacao.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Fornecedor não encontrado"
            })

        fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)
        if not fornecedor:
            return templates.TemplateResponse("admin/verificacao.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Dados do fornecedor não encontrados"
            })

        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor
        })
    except Exception as e:
        logger.error("Erro ao carregar verificação: ", erro=e)
        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar dados do fornecedor"
        })

@router.get("/admin/verificacao")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def verificacao_fornecedores(request: Request, usuario_logado: dict = {}):
    """Lista fornecedores pendentes de verificação"""
    try:
        fornecedores = fornecedor_repo.obter_fornecedores_por_pagina(1, 100)
        fornecedores_pendentes = [f for f in fornecedores if not f.verificado]

        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedores_pendentes": fornecedores_pendentes
        })
    except Exception as e:
        logger.error("Erro ao carregar verificação: ", erro=e)
        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar fornecedores pendentes"
        })

@router.post("/admin/verificacao/{id_fornecedor}/aprovar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def aprovar_fornecedor(request: Request, id_fornecedor: int, usuario_logado: dict = {}):
    """Aprova um fornecedor"""
    try:
        fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)
        if not fornecedor:
            return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

        fornecedor.verificado = True
        from datetime import datetime
        fornecedor.data_verificacao = datetime.now().isoformat()
        fornecedor_repo.atualizar(fornecedor)

        informar_sucesso(request, "Fornecedor aprovado com sucesso!")
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error("Erro ao aprovar fornecedor: ", erro=e)
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/verificacao/{id_fornecedor}/rejeitar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def rejeitar_fornecedor(request: Request, id_fornecedor: int, observacoes: str = Form(""), usuario_logado: dict = {}):
    """Rejeita um fornecedor"""
    try:
        fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)
        if not fornecedor:
            return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

        # Rejeitar fornecedor (remover verificação)
        fornecedor.verificado = False
        fornecedor.data_verificacao = None
        sucesso = fornecedor_repo.atualizar(fornecedor)

        if not sucesso:
            logger.warning("Falha ao rejeitar fornecedor", fornecedor_id=id_fornecedor)

        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error("Erro ao rejeitar fornecedor: ", erro=e)
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

# ==================== GESTÃO DE ITENS (VISUALIZAÇÃO E CONTROLE) ====================

@router.get("/admin/itens")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_itens(
    request: Request,
    pagina: int = 1,
    usuario_logado: dict = {}
):
    """Lista todos os itens do sistema com filtros e paginação"""
    try:
        import math

        # Obter parâmetros de filtro da URL
        busca = request.query_params.get("search", "").strip()
        tipo_item = request.query_params.get("tipo_item", "").strip()
        status_filtro = request.query_params.get("status", "").strip()
        categoria_id = request.query_params.get("categoria", "").strip()
        tamanho_pagina = 10

        # Aplicar filtros se fornecidos, senão listar todos
        if busca or tipo_item or status_filtro or categoria_id:
            itens, total_itens = item_repo.buscar_itens_paginado_repo(
                busca=busca,
                tipo_item=tipo_item,
                status=status_filtro,
                categoria_id=categoria_id,
                pagina=pagina,
                tamanho_pagina=tamanho_pagina
            )
        else:
            itens, total_itens = item_repo.obter_itens_paginado_repo(
                pagina=pagina,
                tamanho_pagina=tamanho_pagina
            )

        # Calcular total de páginas
        total_paginas = math.ceil(total_itens / tamanho_pagina) if total_itens > 0 else 1

        # Buscar dados das categorias para exibir nomes
        categorias_dados = {}
        for item in itens:
            if item.id_categoria and item.id_categoria not in categorias_dados:
                try:
                    categoria = categoria_repo.obter_por_id(item.id_categoria)
                    if categoria:
                        categorias_dados[item.id_categoria] = categoria
                except Exception as e:
                    logger.error("Erro ao buscar categoria", categoria_id=item.id_categoria, erro=e)
                    continue

        # Buscar todas as categorias para o filtro
        categorias = categoria_repo.buscar_categorias()

        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "itens": itens,
            "categorias_dados": categorias_dados,
            "categorias": categorias,
            "tipos_item": [tipo for tipo in TipoFornecimento],
            "total_itens": total_itens,
            "pagina_atual": pagina,
            "total_paginas": total_paginas,
            "busca": busca,
            "tipo_item": tipo_item,
            "status_filtro": status_filtro,
            "categoria_id": categoria_id
        })
    except Exception as e:
        logger.error("Erro ao listar itens: ", erro=e)
        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar itens",
            "itens": [],
            "total_itens": 0,
            "pagina_atual": 1,
            "total_paginas": 1
        })

@router.get("/admin/item/{id_item}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def visualizar_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Visualiza detalhes de um item específico"""
    try:
        item = item_repo.obter_por_id(id_item)

        if not item:
            return templates.TemplateResponse("admin/itens.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Item não encontrado"
            })

        # Buscar dados do fornecedor
        fornecedor = fornecedor_repo.obter_por_id(item.id_fornecedor)

        return templates.TemplateResponse("admin/item_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "item": item,
            "fornecedor": fornecedor
        })
    except Exception as e:
        logger.error("Erro ao visualizar item: ", erro=e)
        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar item"
        })

@router.get("/admin/item/{id_item}/ativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def ativar_item_admin(request: Request, id_item: int, usuario_logado: dict = {}):
    """Ativa um item (admin pode ativar qualquer item)"""
    try:
        sucesso = item_repo.ativar_item_admin(id_item)

        if sucesso:
            informar_sucesso(request, "Item ativado com sucesso!")
        else:
            informar_erro(request, "Erro ao ativar item. Item não encontrado.")

        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        informar_erro(request, f"Erro ao ativar item: {str(e)}")
        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/item/{id_item}/desativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def desativar_item_admin(request: Request, id_item: int, usuario_logado: dict = {}):
    """Desativa um item (admin pode desativar qualquer item)"""
    try:
        sucesso = item_repo.desativar_item_admin(id_item)

        if sucesso:
            informar_sucesso(request, "Item desativado com sucesso!")
        else:
            informar_erro(request, "Erro ao desativar item. Item não encontrado.")

        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        informar_erro(request, f"Erro ao desativar item: {str(e)}")
        return RedirectResponse("/admin/itens", status_code=status.HTTP_303_SEE_OTHER)

# ==================== RELATÓRIOS ====================

@router.get("/admin/relatorios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def relatorios(request: Request, usuario_logado: dict = {}):
    """Página de relatórios e estatísticas"""
    try:
        # Estatísticas gerais do sistema
        stats_gerais = {
            "total_usuarios": usuario_repo.contar(),
            "total_noivos": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.NOIVO),
            "total_admins": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.ADMIN),
            "total_fornecedores": fornecedor_repo.contar(),
            "fornecedores_verificados": fornecedor_repo.contar() - fornecedor_repo.contar_nao_verificados(),
            "fornecedores_nao_verificados": fornecedor_repo.contar_nao_verificados(),
            "total_itens": item_repo.contar(),
            "total_categorias": categoria_repo.contar(),
            "total_orcamentos": orcamento_repo.contar(),
            "total_demandas": demanda_repo.contar()
        }

        # Estatísticas de itens por tipo
        stats_itens = {
            "produtos": item_repo.contar_itens_por_tipo(TipoFornecimento.PRODUTO),
            "servicos": item_repo.contar_itens_por_tipo(TipoFornecimento.SERVICO),
            "espacos": item_repo.contar_itens_por_tipo(TipoFornecimento.ESPACO),
            "detalhes_por_tipo": item_repo.obter_estatisticas_itens()
        }

        # Estatísticas de fornecedores por categoria
        try:
            fornecedores = fornecedor_repo.obter_fornecedores_por_pagina(1, 1000)
            stats_fornecedores = {
                "total": len(fornecedores),
                "verificados": len([f for f in fornecedores if f.verificado]),
                "nao_verificados": len([f for f in fornecedores if not f.verificado])
            }
        except:
            stats_fornecedores = {
                "total": 0,
                "verificados": 0,
                "nao_verificados": 0
            }

        # Calcular percentuais
        total_usuarios = stats_gerais["total_usuarios"]
        percentuais = {
            "noivos": round((stats_gerais["total_noivos"] / total_usuarios * 100) if total_usuarios > 0 else 0, 1),
            "fornecedores": round((stats_gerais["total_fornecedores"] / total_usuarios * 100) if total_usuarios > 0 else 0, 1),
            "admins": round((stats_gerais["total_admins"] / total_usuarios * 100) if total_usuarios > 0 else 0, 1),
            "fornecedores_verificados": round((stats_gerais["fornecedores_verificados"] / stats_gerais["total_fornecedores"] * 100) if stats_gerais["total_fornecedores"] > 0 else 0, 1)
        }

        return templates.TemplateResponse("admin/relatorios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats_gerais": stats_gerais,
            "stats_itens": stats_itens,
            "stats_fornecedores": stats_fornecedores,
            "percentuais": percentuais
        })
    except Exception as e:
        logger.error("Erro ao gerar relatórios: ", erro=e)
        return templates.TemplateResponse("admin/relatorios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao gerar relatórios"
        })

@router.get("/admin/relatorios/exportar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def exportar_relatorios(request: Request, formato: str = "json", usuario_logado: dict = {}):
    """Exporta relatórios em formato JSON ou CSV"""
    try:
        from fastapi.responses import JSONResponse, PlainTextResponse
        from datetime import datetime

        # Coletar todos os dados
        dados = {
            "data_geracao": datetime.now().isoformat(),
            "sistema": {
                "total_usuarios": usuario_repo.contar(),
                "total_noivos": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.NOIVO),
                "total_admins": usuario_repo.contar_usuarios_por_tipo(TipoUsuario.ADMIN),
                "total_fornecedores": fornecedor_repo.contar(),
                "fornecedores_verificados": fornecedor_repo.contar() - fornecedor_repo.contar_nao_verificados(),
                "fornecedores_nao_verificados": fornecedor_repo.contar_nao_verificados(),
                "total_itens": item_repo.contar(),
                "total_categorias": categoria_repo.contar(),
                "total_orcamentos": orcamento_repo.contar(),
                "total_demandas": demanda_repo.contar()
            },
            "itens": {
                "produtos": item_repo.contar_itens_por_tipo(TipoFornecimento.PRODUTO),
                "servicos": item_repo.contar_itens_por_tipo(TipoFornecimento.SERVICO),
                "espacos": item_repo.contar_itens_por_tipo(TipoFornecimento.ESPACO),
                "detalhes": item_repo.obter_estatisticas_itens()
            }
        }

        if formato.lower() == "csv":
            # Gerar CSV
            csv_content = "Categoria,Subcategoria,Valor\n"

            # Dados do sistema
            for chave, valor in dados["sistema"].items():
                csv_content += f"Sistema,{chave.replace('_', ' ').title()},{valor}\n"

            # Dados de itens
            for chave, valor in dados["itens"].items():
                if chave != "detalhes":
                    csv_content += f"Itens,{chave.replace('_', ' ').title()},{valor}\n"

            # Detalhes dos itens
            if dados["itens"]["detalhes"]:
                for item in dados["itens"]["detalhes"]:
                    csv_content += f"Detalhes Itens,{item['tipo']},{item['quantidade']}\n"
                    csv_content += f"Detalhes Preços,{item['tipo']} - Médio,{item['preco_medio']}\n"
                    csv_content += f"Detalhes Preços,{item['tipo']} - Mínimo,{item['preco_minimo']}\n"
                    csv_content += f"Detalhes Preços,{item['tipo']} - Máximo,{item['preco_maximo']}\n"

            return PlainTextResponse(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=relatorio_case_bem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
            )
        else:
            # Retornar JSON
            return JSONResponse(content=dados)

    except Exception as e:
        logger.error("Erro ao exportar relatórios: ", erro=e)
        return JSONResponse(
            content={"erro": "Erro ao exportar relatórios"},
            status_code=500
        )

# ==================== CATEGORIAS DE ITEM ====================

@router.get("/admin/categorias")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_categorias(
    request: Request,
    pagina: int = 1,
    usuario_logado: dict = {}
):
    """Lista todas as categorias de item com filtros e paginação"""
    try:
        import math

        # Obter parâmetros de filtro da URL
        busca = request.query_params.get("search", "").strip()
        tipo_fornecimento = request.query_params.get("tipo_fornecimento", "").strip()
        status_filtro = request.query_params.get("status", "").strip()
        tamanho_pagina = 10

        # Aplicar filtros se fornecidos, senão listar todas
        if busca or tipo_fornecimento or status_filtro:
            categorias, total_categorias = categoria_repo.buscar_categorias_paginado(
                busca=busca,
                tipo_fornecimento=tipo_fornecimento,
                status=status_filtro,
                pagina=pagina,
                tamanho_pagina=tamanho_pagina
            )
        else:
            categorias, total_categorias = categoria_repo.obter_categorias_paginado(
                pagina=pagina,
                tamanho_pagina=tamanho_pagina
            )

        # Calcular total de páginas
        total_paginas = math.ceil(total_categorias / tamanho_pagina) if total_categorias > 0 else 1

        return templates.TemplateResponse("admin/categorias.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categorias": categorias,
            "tipos_item": [tipo for tipo in TipoFornecimento],
            "total_categorias": total_categorias,
            "pagina_atual": pagina,
            "total_paginas": total_paginas,
            "busca": busca,
            "tipo_fornecimento": tipo_fornecimento,
            "status_filtro": status_filtro
        })
    except Exception as e:
        logger.error("Erro ao listar categorias: ", erro=e)
        return templates.TemplateResponse("admin/categorias.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar categorias",
            "categorias": [],
            "total_categorias": 0,
            "pagina_atual": 1,
            "total_paginas": 1
        })

@router.get("/admin/categoria/nova")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def nova_categoria(request: Request, usuario_logado: dict = {}):
    """Formulário para criar nova categoria"""
    return templates.TemplateResponse("admin/categoria_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "tipos_item": [tipo for tipo in TipoFornecimento],
        "acao": "criar"
    })

@router.post("/admin/categoria/criar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def criar_categoria(
    request: Request,
    nome: str = Form(...),
    tipo_fornecimento: str = Form(...),
    descricao: str = Form(""),
    ativo: bool = Form(True),
    usuario_logado: dict = {}
):
    """Cria uma nova categoria"""
    try:
        # Validar se o nome não está vazio
        nome = nome.strip()
        if not nome:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoFornecimento],
                "acao": "criar",
                "erro": "Nome da categoria é obrigatório"
            })

        # Verificar se já existe categoria com o mesmo nome e tipo
        todas_categorias = categoria_repo.buscar_categorias()
        categoria_existente = next((c for c in todas_categorias if c.nome.lower() == nome.lower() and c.tipo_fornecimento == TipoFornecimento(tipo_fornecimento)), None)
        if categoria_existente:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoFornecimento],
                "acao": "criar",
                "erro": f"Já existe uma categoria '{nome}' para o tipo {tipo_fornecimento.capitalize()}"
            })

        categoria = Categoria(
            id=0,
            nome=nome,
            tipo_fornecimento=TipoFornecimento(tipo_fornecimento),
            descricao=descricao if descricao else None,
            ativo=ativo
        )

        categoria_id = categoria_repo.inserir(categoria)
        if categoria_id:
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoFornecimento],
                "acao": "criar",
                "erro": "Erro ao criar categoria"
            })
    except Exception as e:
        logger.error("Erro ao criar categoria: ", erro=e)
        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "tipos_item": [tipo for tipo in TipoFornecimento],
            "acao": "criar",
            "erro": "Erro ao criar categoria"
        })

@router.get("/admin/categoria/editar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def editar_categoria(request: Request, id_categoria: int, usuario_logado: dict = {}):
    """Formulário para editar categoria"""
    try:
        categoria = categoria_repo.obter_por_id(id_categoria)
        if not categoria:
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categoria": categoria,
            "tipos_item": [tipo for tipo in TipoFornecimento],
            "acao": "editar"
        })
    except Exception as e:
        logger.error("Erro ao carregar categoria para edição: ", erro=e)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/categoria/atualizar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def atualizar_categoria(
    request: Request,
    id_categoria: int,
    nome: str = Form(...),
    tipo_fornecimento: str = Form(...),
    descricao: str = Form(""),
    ativo: bool = Form(True),
    usuario_logado: dict = {}
):
    """Atualiza uma categoria existente"""
    try:
        # Validar se o nome não está vazio
        nome = nome.strip()
        if not nome:
            categoria_atual = categoria_repo.obter_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoFornecimento],
                "acao": "editar",
                "erro": "Nome da categoria é obrigatório"
            })

        # Verificar se já existe outra categoria com o mesmo nome e tipo
        todas_categorias = categoria_repo.buscar_categorias()
        categoria_existente = next((c for c in todas_categorias if c.nome.lower() == nome.lower() and c.tipo_fornecimento == TipoFornecimento(tipo_fornecimento)), None)
        if categoria_existente and categoria_existente.id != id_categoria:
            categoria_atual = categoria_repo.obter_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoFornecimento],
                "acao": "editar",
                "erro": f"Já existe outra categoria '{nome}' para o tipo {tipo_fornecimento.capitalize()}"
            })

        categoria = Categoria(
            id=id_categoria,
            nome=nome,
            tipo_fornecimento=TipoFornecimento(tipo_fornecimento),
            descricao=descricao if descricao else None,
            ativo=ativo
        )

        if categoria_repo.atualizar(categoria):
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
        else:
            categoria_atual = categoria_repo.obter_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoFornecimento],
                "acao": "editar",
                "erro": "Erro ao atualizar categoria"
            })
    except Exception as e:
        logger.error("Erro ao atualizar categoria: ", erro=e)
        categoria_atual = categoria_repo.obter_por_id(id_categoria)
        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categoria": categoria_atual,
            "tipos_item": [tipo for tipo in TipoFornecimento],
            "acao": "editar",
            "erro": "Erro ao atualizar categoria"
        })

@router.post("/admin/categoria/excluir/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def excluir_categoria(request: Request, id_categoria: int, usuario_logado: dict = {}):
    """Exclui uma categoria"""
    try:
        categoria_repo.excluir(id_categoria)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error("Erro ao excluir categoria: ", erro=e)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/categoria/{id_categoria}/ativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def ativar_categoria(request: Request, id_categoria: int, usuario_logado: dict = {}):
    """Ativa uma categoria"""
    try:
        sucesso = categoria_repo.ativar_categoria(id_categoria)
        if not sucesso:
            logger.error("Falha ao ativar categoria", categoria_id=id_categoria)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error("Erro ao ativar categoria: ", erro=e)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/categoria/{id_categoria}/desativar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def desativar_categoria(request: Request, id_categoria: int, usuario_logado: dict = {}):
    """Desativa uma categoria"""
    try:
        sucesso = categoria_repo.desativar_categoria(id_categoria)
        if not sucesso:
            logger.error("Falha ao desativar categoria", categoria_id=id_categoria)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error("Erro ao desativar categoria: ", erro=e)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

# ==================== CONFIGURAÇÕES ====================

@router.get("/admin/configuracoes")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def configuracoes(request: Request, usuario_logado: dict = {}):
    """Página de configurações do sistema"""
    return templates.TemplateResponse("admin/configuracoes.html", {
        "request": request,
        "usuario_logado": usuario_logado
    })