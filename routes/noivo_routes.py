from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from infrastructure.security import requer_autenticacao
from core.models.usuario_model import TipoUsuario
from core.models.demanda_model import Demanda
from core.repositories import (
    usuario_repo,
    item_repo,
    demanda_repo,
    orcamento_repo,
    casal_repo,
    favorito_repo,
    fornecedor_repo,
    item_orcamento_repo,
)
from util.flash_messages import informar_sucesso, informar_erro
from util.template_helpers import configurar_filtros_jinja
from util.error_handlers import tratar_erro_rota
from infrastructure.logging import logger
from util.pagination import PaginationHelper

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

# Importar função centralizada de route_helpers
from util.route_helpers import get_active_page


def get_noivo_active_page(request: Request) -> str:
    """
    Determina qual página está ativa na área noivo.
    DEPRECATED: Usa get_active_page do route_helpers.
    Mantido para compatibilidade.
    """
    return get_active_page(request, "noivo")


# ==================== REDIRECIONAMENTO RAIZ ====================


@router.get("/noivo")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def noivo_root(request: Request, usuario_logado: dict = {}):
    """Redireciona /noivo para /noivo/dashboard"""
    return RedirectResponse("/noivo/dashboard", status_code=status.HTTP_302_FOUND)


# ==================== DASHBOARD ====================


@router.get("/noivo/dashboard")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/dashboard.html")
async def dashboard_noivo(request: Request, usuario_logado: dict = {}):
    """Dashboard principal dos noivos"""
    id_noivo = usuario_logado["id"]
    logger.info("Carregando dashboard do noivo", noivo_id=id_noivo)

    # Buscar dados do noivo
    noivo = usuario_repo.obter_por_id(id_noivo)

    # Buscar dados do casal
    try:
        casal = casal_repo.obter_por_noivo(id_noivo)
    except Exception as e:
        logger.warning("Casal não encontrado para noivo", noivo_id=id_noivo, erro=e)
        casal = None

    # Buscar demandas do casal
    try:
        if casal:
            demandas_casal = demanda_repo.obter_por_casal(casal.id)
            demandas_ativas = [d for d in demandas_casal if d.status.value == "ATIVA"]
            demandas_recentes = demandas_casal[:5]
        else:
            demandas_casal = []
            demandas_ativas = []
            demandas_recentes = []
    except Exception as e:
        logger.error(
            "Erro ao buscar demandas do casal",
            casal_id=casal.id if casal else None,
            erro=e,
        )
        demandas_casal = []
        demandas_ativas = []
        demandas_recentes = []

    # Buscar orçamentos do noivo
    try:
        orcamentos_recebidos = orcamento_repo.obter_por_noivo(id_noivo)
        orcamentos_pendentes = [
            o for o in orcamentos_recebidos if o.status == "PENDENTE"
        ]
    except Exception as e:
        logger.error("Erro ao buscar orçamentos do noivo", noivo_id=id_noivo, erro=e)
        orcamentos_recebidos = []
        orcamentos_pendentes = []

    # Estatísticas para o noivo
    stats = {
        "total_demandas": len(demandas_casal),
        "demandas_ativas": len(demandas_ativas),
        "orcamentos_recebidos": len(orcamentos_recebidos),
        "orcamentos_pendentes": len(orcamentos_pendentes),
        "favoritos": favorito_repo.contar_por_noivo(id_noivo),
        "total_fornecedores": fornecedor_repo.contar(),
    }

    return templates.TemplateResponse(
        "noivo/dashboard.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "noivo": noivo,
            "casal": casal,
            "stats": stats,
            "demandas_recentes": demandas_recentes,
        },
    )


# ==================== EXPLORAR ITENS ====================


@router.get("/noivo/produtos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/produtos.html")
async def listar_produtos(request: Request, usuario_logado: dict = {}):
    """Lista produtos disponíveis"""
    logger.info("Listando produtos", noivo_id=usuario_logado["id"])
    produtos = item_repo.obter_produtos()

    return templates.TemplateResponse(
        "noivo/produtos.html",
        {"request": request, "usuario_logado": usuario_logado, "produtos": produtos},
    )


@router.get("/noivo/servicos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/servicos.html")
async def listar_servicos(request: Request, usuario_logado: dict = {}):
    """Lista serviços disponíveis"""
    logger.info("Listando serviços", noivo_id=usuario_logado["id"])
    servicos = item_repo.obter_servicos()

    return templates.TemplateResponse(
        "noivo/servicos.html",
        {"request": request, "usuario_logado": usuario_logado, "servicos": servicos},
    )


@router.get("/noivo/espacos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/espacos.html")
async def listar_espacos(request: Request, usuario_logado: dict = {}):
    """Lista espaços disponíveis"""
    logger.info("Listando espaços", noivo_id=usuario_logado["id"])
    espacos = item_repo.obter_espacos()

    return templates.TemplateResponse(
        "noivo/espacos.html",
        {"request": request, "usuario_logado": usuario_logado, "espacos": espacos},
    )


@router.get("/noivo/buscar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/buscar.html")
async def buscar_itens(request: Request, q: str = "", usuario_logado: dict = {}):
    """Busca itens por termo"""
    logger.info("Buscando itens", noivo_id=usuario_logado["id"], termo=q)

    resultados = []
    if q.strip():
        resultados = item_repo.buscar_itens(q.strip())

    return templates.TemplateResponse(
        "noivo/buscar.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "resultados": resultados,
            "termo_busca": q,
        },
    )


# ==================== DETALHES DE ITENS ====================


@router.get("/noivo/item/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/item_nao_encontrado.html")
async def visualizar_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Visualiza detalhes de um item"""
    logger.info("Visualizando item", noivo_id=usuario_logado["id"], item_id=id_item)

    item = item_repo.obter_por_id(id_item)

    if not item or not item.ativo:
        logger.warning(
            "Item não encontrado ou inativo",
            item_id=id_item,
            ativo=item.ativo if item else None,
        )
        return templates.TemplateResponse(
            "noivo/item_nao_encontrado.html",
            {"request": request, "usuario_logado": usuario_logado},
        )

    # Buscar dados do fornecedor
    fornecedor = None
    try:
        fornecedor = fornecedor_repo.obter_por_id(item.id_fornecedor)
    except Exception as e:
        logger.error(
            "Erro ao buscar fornecedor do item",
            item_id=id_item,
            fornecedor_id=item.id_fornecedor,
            erro=e,
        )

    return templates.TemplateResponse(
        "noivo/item_detalhes.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "item": item,
            "fornecedor": fornecedor,
        },
    )


# ==================== DEMANDAS ====================


@router.get("/noivo/demandas")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/demandas.html")
async def listar_demandas(
    request: Request, status: str = "", search: str = "", usuario_logado: dict = {}
):
    """Lista demandas do noivo"""
    id_noivo = usuario_logado["id"]
    logger.info(
        "Listando demandas do noivo",
        noivo_id=id_noivo,
        filtro_status=status,
        filtro_search=search,
    )

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)
    if not casal:
        logger.warning("Casal não encontrado para noivo", noivo_id=id_noivo)
        return templates.TemplateResponse(
            "noivo/demandas.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Casal não encontrado",
            },
        )

    # Buscar demandas do casal
    demandas = demanda_repo.obter_por_casal(casal.id)

    # Aplicar filtros
    if status:
        demandas = [d for d in demandas if d.status.value == status]

    if search:
        demandas = [
            d
            for d in demandas
            if search.lower() in d.titulo.lower()
            or search.lower() in d.descricao.lower()
        ]

    return templates.TemplateResponse(
        "noivo/demandas.html",
        {"request": request, "usuario_logado": usuario_logado, "demandas": demandas},
    )


@router.get("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def nova_demanda_form(request: Request, usuario_logado: dict = {}):
    """Formulário para criar nova demanda"""
    return templates.TemplateResponse(
        "noivo/demanda_form.html",
        {"request": request, "usuario_logado": usuario_logado, "acao": "criar"},
    )


@router.post("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/demanda_form.html")
async def criar_demanda(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    id_categoria: int = Form(...),
    orcamento_min: float = Form(None),
    orcamento_max: float = Form(None),
    prazo_entrega: str = Form(""),
    observacoes: str = Form(""),
    usuario_logado: dict = {},
):
    """Cria uma nova demanda"""
    id_noivo = usuario_logado["id"]
    logger.info("Criando nova demanda", noivo_id=id_noivo, titulo=titulo)

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)
    if not casal:
        logger.warning("Casal não encontrado ao criar demanda", noivo_id=id_noivo)
        return templates.TemplateResponse(
            "noivo/demanda_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Casal não encontrado",
                "acao": "criar",
            },
        )

    # Criar nova demanda
    nova_demanda = Demanda(
        id=0,  # Será definido pelo banco
        id_casal=casal.id,
        id_categoria=id_categoria,
        titulo=titulo,
        descricao=descricao,
        orcamento_min=orcamento_min if orcamento_min else None,
        orcamento_max=orcamento_max if orcamento_max else None,
        prazo_entrega=prazo_entrega if prazo_entrega else None,
        observacoes=observacoes if observacoes else None,
    )

    # Inserir no banco
    id_demanda = demanda_repo.inserir(nova_demanda)

    if id_demanda:
        logger.info(
            "Demanda criada com sucesso", demanda_id=id_demanda, casal_id=casal.id
        )
        return RedirectResponse(
            "/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        logger.error(
            "Falha ao inserir demanda no banco", casal_id=casal.id, titulo=titulo
        )
        return templates.TemplateResponse(
            "noivo/demanda_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao criar demanda no banco de dados",
                "acao": "criar",
            },
        )


# ==================== ORÇAMENTOS ====================


@router.get("/noivo/orcamentos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/orcamentos.html")
async def listar_orcamentos(
    request: Request,
    status: str = "",
    demanda: str = "",
    search: str = "",
    usuario_logado: dict = {},
):
    """Lista orçamentos recebidos"""
    id_noivo = usuario_logado["id"]
    logger.info(
        "Listando orçamentos do noivo",
        noivo_id=id_noivo,
        filtro_status=status,
        filtro_demanda=demanda,
    )

    # Buscar orçamentos do noivo
    orcamentos = orcamento_repo.obter_por_noivo(id_noivo)

    # Aplicar filtros
    if status:
        orcamentos = [o for o in orcamentos if o.status == status]

    if demanda:
        orcamentos = [o for o in orcamentos if str(o.id_demanda) == demanda]

    if search:
        # Buscar por nome do fornecedor (precisamos buscar os dados do fornecedor)
        orcamentos_filtrados = []
        for orcamento in orcamentos:
            try:
                fornecedor = fornecedor_repo.obter_por_id(orcamento.id_fornecedor_prestador)
                if fornecedor and search.lower() in fornecedor.nome.lower():
                    orcamentos_filtrados.append(orcamento)
            except Exception as e:
                logger.warning(
                    "Erro ao buscar fornecedor para filtro",
                    orcamento_id=orcamento.id,
                    fornecedor_id=orcamento.id_fornecedor_prestador,
                    erro=e,
                )
                continue
        orcamentos = orcamentos_filtrados

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    # Buscar demandas do casal para o filtro
    minhas_demandas = demanda_repo.obter_por_casal(casal.id) if casal else []

    # Enriquecer orçamentos com dados adicionais
    orcamentos_enriched = []
    for orcamento in orcamentos:
        try:
            # Buscar dados da demanda
            demanda_data = demanda_repo.obter_por_id(orcamento.id_demanda)
            # Buscar dados do fornecedor
            fornecedor_data = fornecedor_repo.obter_por_id(orcamento.id_fornecedor_prestador)
            # Buscar itens do orçamento
            itens_orcamento = item_orcamento_repo.obter_por_orcamento(orcamento.id)

            orcamento_dict = {
                "id": orcamento.id,
                "id_demanda": orcamento.id_demanda,
                "id_fornecedor": orcamento.id_fornecedor_prestador,
                "status": orcamento.status,
                "valor_total": orcamento.valor_total,
                "data_envio": orcamento.data_hora_cadastro,
                "prazo_entrega": orcamento.data_hora_validade,
                "observacoes": orcamento.observacoes,
                "demanda_titulo": (
                    demanda_data.titulo if demanda_data else "Demanda não encontrada"
                ),
                "fornecedor_nome": (
                    fornecedor_data.nome
                    if fornecedor_data
                    else "Fornecedor não encontrado"
                ),
                "itens_count": len(itens_orcamento),
            }
            orcamentos_enriched.append(orcamento_dict)
        except Exception as e:
            logger.error(
                "Erro ao enriquecer orçamento", orcamento_id=orcamento.id, erro=e
            )
            continue

    return templates.TemplateResponse(
        "noivo/orcamentos.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamentos": orcamentos_enriched,
            "minhas_demandas": minhas_demandas,
        },
    )



@router.get("/noivo/orcamentos/{id_orcamento}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/orcamentos")
async def visualizar_orcamento(
    request: Request, id_orcamento: int, usuario_logado: dict = {}
):
    """Visualiza detalhes de um orçamento"""
    id_noivo = usuario_logado["id"]
    logger.info("Visualizando orçamento", noivo_id=id_noivo, orcamento_id=id_orcamento)

    # Buscar orçamento
    orcamento = orcamento_repo.obter_por_id(id_orcamento)
    if not orcamento:
        logger.warning("Orçamento não encontrado", orcamento_id=id_orcamento)
        return RedirectResponse(
            "/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER
        )

    # Buscar demanda relacionada
    demanda = demanda_repo.obter_por_id(orcamento.id_demanda)

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    if not demanda or not casal or demanda.id_casal != casal.id:
        # Verificar se o orçamento pertence ao casal do noivo logado
        logger.warning(
            "Acesso negado ao orçamento",
            orcamento_id=id_orcamento,
            noivo_id=id_noivo,
            demanda_casal_id=demanda.id_casal if demanda else None,
            casal_id=casal.id if casal else None,
        )
        return RedirectResponse(
            "/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER
        )

    # Buscar fornecedor
    fornecedor = fornecedor_repo.obter_por_id(orcamento.id_fornecedor)

    # Buscar itens do orçamento
    itens_orcamento = item_orcamento_repo.obter_por_orcamento(orcamento.id)

    # Enriquecer itens com dados do item
    itens_enriched = []
    for item_orc in itens_orcamento:
        try:
            item_data = item_repo.obter_por_id(item_orc["id_item"])
            item_dict = {
                "id_item": item_orc["id_item"],
                "nome_item": item_data.nome if item_data else "Item não encontrado",
                "descricao_item": item_data.descricao if item_data else "",
                "tipo_item": item_data.tipo.value if item_data else "",
                "quantidade": item_orc["quantidade"],
                "preco_unitario": item_orc["preco_unitario"],
                "desconto": item_orc.get("desconto", 0) or 0,
                "preco_total": item_orc["preco_total"],
                "observacoes": item_orc.get("observacoes"),
            }
            itens_enriched.append(item_dict)
        except Exception as e:
            logger.error(
                "Erro ao enriquecer item do orçamento",
                orcamento_id=id_orcamento,
                item_id=item_orc.get("id_item"),
                erro=e,
            )
            continue

    # Criar objeto orçamento enriquecido
    orcamento_enriched = {
        "id": orcamento.id,
        "id_demanda": orcamento.id_demanda,
        "id_fornecedor": orcamento.id_fornecedor_prestador,
        "status": orcamento.status,
        "valor_total": orcamento.valor_total,
        "data_envio": orcamento.data_hora_cadastro,
        "prazo_entrega": orcamento.data_hora_validade,
        "observacoes": orcamento.observacoes,
        "desconto": getattr(orcamento, "desconto", 0) or 0,
        "data_resposta": getattr(orcamento, "data_resposta", None),
        "itens": itens_enriched,
    }

    return templates.TemplateResponse(
        "noivo/orcamento_detalhes.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamento": orcamento_enriched,
            "demanda": demanda,
            "fornecedor": fornecedor,
        },
    )


@router.post("/noivo/orcamentos/{id_orcamento}/aceitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/orcamentos")
async def aceitar_orcamento(
    request: Request, id_orcamento: int, usuario_logado: dict = {}
):
    """Aceita um orçamento"""
    logger.info(
        "Aceitando orçamento", noivo_id=usuario_logado["id"], orcamento_id=id_orcamento
    )

    # Buscar o orçamento para obter o id_demanda
    orcamento = orcamento_repo.obter_por_id(id_orcamento)
    if not orcamento:
        logger.warning("Orçamento não encontrado ao aceitar", orcamento_id=id_orcamento)
        informar_erro(request, "Orçamento não encontrado!")
        return RedirectResponse(
            "/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER
        )

    # Aceitar este orçamento e rejeitar os outros da mesma demanda
    sucesso = orcamento_repo.aceitar_e_rejeitar_outros(
        id_orcamento, orcamento.id_demanda
    )

    if sucesso:
        logger.info(
            "Orçamento aceito com sucesso",
            orcamento_id=id_orcamento,
            demanda_id=orcamento.id_demanda,
        )
        informar_sucesso(request, "Orçamento aceito com sucesso!")
    else:
        logger.error(
            "Falha ao aceitar orçamento",
            orcamento_id=id_orcamento,
            demanda_id=orcamento.id_demanda,
        )
        informar_erro(request, "Erro ao aceitar orçamento!")

    return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/noivo/orcamentos/{id_orcamento}/rejeitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/orcamentos")
async def rejeitar_orcamento(
    request: Request, id_orcamento: int, usuario_logado: dict = {}
):
    """Rejeita um orçamento"""
    logger.info(
        "Rejeitando orçamento", noivo_id=usuario_logado["id"], orcamento_id=id_orcamento
    )

    # Rejeitar o orçamento
    sucesso = orcamento_repo.rejeitar(id_orcamento)

    if sucesso:
        logger.info("Orçamento rejeitado com sucesso", orcamento_id=id_orcamento)
        informar_sucesso(request, "Orçamento rejeitado com sucesso!")
    else:
        logger.error("Falha ao rejeitar orçamento", orcamento_id=id_orcamento)
        informar_erro(request, "Erro ao rejeitar orçamento!")

    return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)


# ==================== PERFIL E CASAL ====================


@router.get("/noivo/perfil")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/perfil.html")
async def perfil_noivo(request: Request, usuario_logado: dict = {}):
    """Página de perfil do noivo"""
    id_noivo = usuario_logado["id"]
    logger.info("Carregando perfil do noivo", noivo_id=id_noivo)

    noivo = usuario_repo.obter_por_id(id_noivo)

    # Buscar dados do casal
    casal = None
    try:
        casal = casal_repo.obter_por_noivo(id_noivo)
    except Exception as e:
        logger.warning(
            "Casal não encontrado para noivo no perfil", noivo_id=id_noivo, erro=e
        )

    return templates.TemplateResponse(
        "noivo/perfil.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "noivo": noivo,
            "casal": casal,
        },
    )


@router.post("/noivo/perfil")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/perfil.html")
async def atualizar_perfil_noivo(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf: str = Form(""),
    data_nascimento: str = Form(""),
    usuario_logado: dict = {},
):
    """Atualiza perfil do noivo"""
    id_noivo = usuario_logado["id"]
    logger.info("Atualizando perfil do noivo", noivo_id=id_noivo, email=email)

    noivo = usuario_repo.obter_por_id(id_noivo)

    if not noivo:
        logger.error("Usuário não encontrado ao atualizar perfil", noivo_id=id_noivo)
        return templates.TemplateResponse(
            "noivo/perfil.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado",
            },
        )

    # Atualizar dados
    noivo.nome = nome
    noivo.email = email
    noivo.telefone = telefone
    noivo.cpf = cpf if cpf else None
    noivo.data_nascimento = data_nascimento if data_nascimento else None

    sucesso = usuario_repo.atualizar(noivo)

    if sucesso:
        logger.info("Perfil atualizado com sucesso", noivo_id=id_noivo)
        return templates.TemplateResponse(
            "noivo/perfil.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "noivo": noivo,
                "sucesso": "Perfil atualizado com sucesso!",
            },
        )
    else:
        logger.error("Falha ao atualizar perfil no banco", noivo_id=id_noivo)
        return templates.TemplateResponse(
            "noivo/perfil.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "noivo": noivo,
                "erro": "Erro ao atualizar perfil",
            },
        )


# ==================== FORNECEDORES ====================


@router.get("/noivo/fornecedores")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_fornecedores(request: Request, usuario_logado: dict = {}):
    """Lista fornecedores verificados para os noivos"""
    try:
        # Parâmetros de filtro
        search = request.query_params.get("search", "").strip()
        tipo = request.query_params.get("tipo", "").strip()
        page = PaginationHelper.get_page_number(request)

        # Buscar todos os fornecedores verificados
        todos_fornecedores = fornecedor_repo.obter_fornecedores_verificados()

        # Aplicar filtros
        fornecedores = todos_fornecedores
        if search:
            fornecedores = [
                f
                for f in fornecedores
                if search.lower() in f.nome.lower()
                or (f.nome_empresa and search.lower() in f.nome_empresa.lower())
                or (f.descricao and search.lower() in f.descricao.lower())
            ]

        # Enriquecer fornecedores com contagem de itens
        fornecedores_enriched = []
        for fornecedor in fornecedores:
            fornecedor_dict = {
                "id": fornecedor.id,
                "nome": fornecedor.nome,
                "nome_empresa": fornecedor.nome_empresa,
                "descricao": fornecedor.descricao,
                "telefone": fornecedor.telefone,
                "email": fornecedor.email,
                "verificado": fornecedor.verificado,
                "total_itens": item_repo.contar_por_fornecedor(fornecedor.id),
            }
            fornecedores_enriched.append(fornecedor_dict)

        # Aplicar paginação
        total = len(fornecedores_enriched)
        start = (page - 1) * PaginationHelper.PUBLIC_PAGE_SIZE
        end = start + PaginationHelper.PUBLIC_PAGE_SIZE
        fornecedores_paginados = fornecedores_enriched[start:end]

        page_info = PaginationHelper.paginate(
            fornecedores_paginados,
            total,
            page,
            PaginationHelper.PUBLIC_PAGE_SIZE
        )

        return templates.TemplateResponse(
            "noivo/fornecedores.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "fornecedores": page_info.items,
                "pagina_atual": page_info.current_page,
                "total_pages": page_info.total_pages,
                "total": page_info.total_items,
            },
        )
    except Exception as e:
        logger.error("Erro ao listar fornecedores", erro=e)
        return templates.TemplateResponse(
            "noivo/fornecedores.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "fornecedores": [],
                "erro": "Erro ao carregar fornecedores",
                "pagina_atual": 1,
                "total_pages": 1,
                "total": 0,
            },
        )


# ==================== FAVORITOS ====================


@router.get("/noivo/favoritos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/favoritos.html")
async def listar_favoritos(request: Request, usuario_logado: dict = {}):
    """Lista itens favoritos do noivo"""
    id_noivo = usuario_logado["id"]
    logger.info("Listando favoritos do noivo", noivo_id=id_noivo)

    favoritos = favorito_repo.obter_por_noivo(id_noivo)

    return templates.TemplateResponse(
        "noivo/favoritos.html",
        {"request": request, "usuario_logado": usuario_logado, "favoritos": favoritos},
    )


@router.post("/noivo/favoritos/adicionar/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def adicionar_favorito(request: Request, id_item: int, usuario_logado: dict = {}):
    """Adiciona um item aos favoritos"""
    id_noivo = usuario_logado["id"]
    logger.info("Adicionando item aos favoritos", noivo_id=id_noivo, item_id=id_item)

    try:
        sucesso = favorito_repo.adicionar(id_noivo, id_item)

        if sucesso:
            logger.info(
                "Favorito adicionado com sucesso", noivo_id=id_noivo, item_id=id_item
            )
            return {"success": True, "message": "Item adicionado aos favoritos"}
        else:
            logger.warning(
                "Falha ao adicionar favorito", noivo_id=id_noivo, item_id=id_item
            )
            return {"success": False, "message": "Erro ao adicionar favorito"}
    except Exception as e:
        logger.error(
            "Erro ao adicionar favorito", noivo_id=id_noivo, item_id=id_item, erro=e
        )
        return {"success": False, "message": "Erro interno"}


@router.post("/noivo/favoritos/remover/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def remover_favorito(request: Request, id_item: int, usuario_logado: dict = {}):
    """Remove um item dos favoritos"""
    id_noivo = usuario_logado["id"]
    logger.info("Removendo item dos favoritos", noivo_id=id_noivo, item_id=id_item)

    try:
        sucesso = favorito_repo.remover(id_noivo, id_item)

        if sucesso:
            logger.info(
                "Favorito removido com sucesso", noivo_id=id_noivo, item_id=id_item
            )
            return {"success": True, "message": "Item removido dos favoritos"}
        else:
            logger.warning(
                "Falha ao remover favorito", noivo_id=id_noivo, item_id=id_item
            )
            return {"success": False, "message": "Erro ao remover favorito"}
    except Exception as e:
        logger.error(
            "Erro ao remover favorito", noivo_id=id_noivo, item_id=id_item, erro=e
        )
        return {"success": False, "message": "Erro interno"}


# ==================== CHECKLIST ====================


@router.get("/noivo/checklist")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def checklist(request: Request, usuario_logado: dict = {}):
    """Exibe o checklist do casamento"""
    try:
        id_noivo = usuario_logado["id"]
        logger.info("Carregando checklist do noivo", noivo_id=id_noivo)

        # Checklist vazio (feature futura)
        categorias = []
        total_tarefas = 0
        tarefas_concluidas = 0
        tarefas_pendentes = 0
        progresso = 0

        return templates.TemplateResponse(
            "noivo/checklist.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "categorias": categorias,
                "total_tarefas": total_tarefas,
                "tarefas_concluidas": tarefas_concluidas,
                "tarefas_pendentes": tarefas_pendentes,
                "progresso": progresso,
            },
        )
    except Exception as e:
        logger.error(
            "Erro ao carregar checklist", noivo_id=usuario_logado["id"], erro=e
        )
        return templates.TemplateResponse(
            "noivo/checklist.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao carregar checklist",
                "categorias": [],
                "total_tarefas": 0,
                "tarefas_concluidas": 0,
                "tarefas_pendentes": 0,
                "progresso": 0,
            },
        )
