from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from infrastructure.security import requer_autenticacao
from core.models.usuario_model import TipoUsuario
from core.models.demanda_model import Demanda
from core.repositories import (
    usuario_repo,
    demanda_repo,
    orcamento_repo,
    casal_repo,
    fornecedor_repo,
    item_orcamento_repo,
)
from util.flash_messages import informar_sucesso, informar_erro
from util.template_helpers import configurar_filtros_jinja
from util.error_handlers import tratar_erro_rota
from infrastructure.logging import logger

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
async def noivo_root(_request: Request, _usuario_logado: dict = {}):
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

            # Enriquecer demandas recentes com contagem de orçamentos
            demandas_recentes = []
            for demanda in demandas_casal[:5]:
                demanda.orcamentos_count = orcamento_repo.contar_por_demanda(demanda.id)  # type: ignore[attr-defined]
                demandas_recentes.append(demanda)
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
            if search.lower() in d.descricao.lower()
        ]

    # Enriquecer demandas com contagens de itens e orçamentos
    from core.repositories import item_demanda_repo
    demandas_com_contagens = []
    for demanda in demandas:
        try:
            # Adicionar atributos de contagem ao objeto demanda
            total_itens = item_demanda_repo.contar_por_demanda(demanda.id)
            demanda.itens_count = total_itens  # type: ignore[attr-defined]
            demanda.orcamentos_count = orcamento_repo.contar_por_demanda(demanda.id)  # type: ignore[attr-defined]
            demanda.orcamentos_pendentes = orcamento_repo.contar_por_demanda_e_status(  # type: ignore[attr-defined]
                demanda.id, "PENDENTE"
            )

            # Calcular quantos itens foram atendidos (têm item_orcamento aceito)
            itens_demanda = item_demanda_repo.obter_por_demanda(demanda.id)
            itens_atendidos = 0
            for item_demanda in itens_demanda:
                try:
                    # Verificar se este item_demanda tem algum item_orcamento ACEITO
                    item_demanda_id = item_demanda.get("id")
                    if item_demanda_id and item_orcamento_repo.verificar_item_demanda_ja_aceito(item_demanda_id):
                        itens_atendidos += 1
                except Exception as e:
                    logger.warning(
                        "Erro ao verificar item_demanda aceito",
                        demanda_id=demanda.id,
                        item_demanda_id=item_demanda.get("id"),
                        erro=e
                    )
                    continue

            demanda.itens_atendidos = itens_atendidos  # type: ignore[attr-defined]

            # Calcular percentual de atendimento
            if total_itens > 0:
                demanda.percentual_atendimento = int((itens_atendidos / total_itens) * 100)  # type: ignore[attr-defined]
            else:
                demanda.percentual_atendimento = 0  # type: ignore[attr-defined]

        except Exception as e:
            logger.error(
                "Erro ao enriquecer demanda com dados de atendimento",
                demanda_id=demanda.id,
                erro=e
            )
            # Garantir que os atributos existam mesmo em caso de erro
            demanda.itens_count = 0  # type: ignore[attr-defined]
            demanda.orcamentos_count = 0  # type: ignore[attr-defined]
            demanda.orcamentos_pendentes = 0  # type: ignore[attr-defined]
            demanda.itens_atendidos = 0  # type: ignore[attr-defined]
            demanda.percentual_atendimento = 0  # type: ignore[attr-defined]

        demandas_com_contagens.append(demanda)

    return templates.TemplateResponse(
        "noivo/demandas.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "demandas": demandas_com_contagens,
        },
    )


@router.get("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def nova_demanda_form(request: Request, usuario_logado: dict = {}):
    """Formulário para criar nova demanda"""
    from core.repositories import categoria_repo
    from core.models.tipo_fornecimento_model import TipoFornecimento

    id_noivo = usuario_logado["id"]

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    # Buscar categorias ativas agrupadas por tipo
    categorias = categoria_repo.buscar_categorias()
    # Usar chaves SEM acento para compatibilidade com JavaScript normalize()
    categorias_por_tipo = {
        "PRODUTO": [{"id": c.id, "nome": c.nome} for c in categorias if c.ativo and c.tipo_fornecimento == TipoFornecimento.PRODUTO],
        "SERVICO": [{"id": c.id, "nome": c.nome} for c in categorias if c.ativo and c.tipo_fornecimento == TipoFornecimento.SERVICO],
        "ESPACO": [{"id": c.id, "nome": c.nome} for c in categorias if c.ativo and c.tipo_fornecimento == TipoFornecimento.ESPACO],
    }

    return templates.TemplateResponse(
        "noivo/demanda_form.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "criar",
            "categorias_por_tipo": categorias_por_tipo,
            "casal": casal,
        },
    )


@router.post("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/demanda_form.html")
async def criar_demanda(
    request: Request,
    descricao: str = Form(...),
    orcamento_total: str = Form(""),
    data_casamento: str = Form(""),
    cidade_casamento: str = Form(""),
    prazo_entrega: str = Form(""),
    observacoes: str = Form(""),
    tipo: list = Form([], alias="tipo[]"),
    id_categoria: list = Form([], alias="id_categoria[]"),
    descricao_item: list = Form([], alias="descricao_item[]"),
    quantidade: list = Form([], alias="quantidade[]"),
    preco_maximo: list = Form([], alias="preco_maximo[]"),
    observacoes_item: list = Form([], alias="observacoes_item[]"),
    usuario_logado: dict = {},
):
    """Cria uma nova demanda com itens (descrições livres)"""
    from core.repositories import item_demanda_repo
    from core.models.item_demanda_model import ItemDemanda

    id_noivo = usuario_logado["id"]
    logger.info("Criando nova demanda", noivo_id=id_noivo, total_itens=len(tipo))

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)
    if not casal:
        logger.warning("Casal não encontrado ao criar demanda", noivo_id=id_noivo)
        informar_erro(request, "Casal não encontrado. Cadastre um casal antes de criar demandas.")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Validar que pelo menos um item foi fornecido
    if not tipo or len(tipo) == 0:
        logger.warning("Tentativa de criar demanda sem itens", noivo_id=id_noivo)
        informar_erro(request, "Adicione pelo menos um item à demanda")
        return RedirectResponse("/noivo/demandas/nova", status_code=status.HTTP_303_SEE_OTHER)

    # Converter orcamento_total de string para float
    orcamento_total_valor = None
    if orcamento_total and orcamento_total.strip():
        try:
            orcamento_total_valor = float(orcamento_total)
        except (ValueError, TypeError):
            logger.warning("Valor de orçamento total inválido", valor=orcamento_total)

    # Criar nova demanda
    nova_demanda = Demanda(
        id=0,  # Será definido pelo banco
        id_casal=casal.id,
        descricao=descricao,
        orcamento_total=orcamento_total_valor,
        data_casamento=data_casamento if data_casamento else casal.data_casamento,
        cidade_casamento=cidade_casamento if cidade_casamento else casal.local_previsto,
        prazo_entrega=prazo_entrega if prazo_entrega else None,
        observacoes=observacoes if observacoes else None,
    )

    # Inserir demanda no banco
    id_demanda = demanda_repo.inserir(nova_demanda)

    if id_demanda:
        # Inserir itens da demanda (descrições livres)
        itens_inseridos = 0
        for i in range(len(tipo)):
            try:
                # Validar e converter valores
                tipo_valor = tipo[i] if i < len(tipo) else None
                id_cat = int(id_categoria[i]) if i < len(id_categoria) and id_categoria[i] else None
                desc_item = descricao_item[i] if i < len(descricao_item) else None
                qtd = int(quantidade[i]) if i < len(quantidade) and quantidade[i] else 1
                preco_max = float(preco_maximo[i]) if i < len(preco_maximo) and preco_maximo[i] else None
                obs_item = observacoes_item[i] if i < len(observacoes_item) and observacoes_item[i] else None

                if tipo_valor and id_cat and desc_item:
                    item_demanda = ItemDemanda(
                        id=0,  # Será definido pelo banco
                        id_demanda=id_demanda,
                        tipo=tipo_valor,
                        id_categoria=id_cat,
                        descricao=desc_item,
                        quantidade=qtd,
                        preco_maximo=preco_max,
                        observacoes=obs_item
                    )
                    item_demanda_repo.inserir(item_demanda)
                    itens_inseridos += 1
            except Exception as e:
                logger.error("Erro ao inserir item da demanda", erro=e, demanda_id=id_demanda, item_index=i)
        logger.info(
            "Demanda criada com sucesso",
            demanda_id=id_demanda,
            casal_id=casal.id,
            total_itens=itens_inseridos
        )
        informar_sucesso(request, f"Demanda criada com sucesso! {itens_inseridos} itens adicionados.")
        return RedirectResponse(
            "/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        logger.error(
            "Falha ao inserir demanda no banco", casal_id=casal.id
        )
        informar_erro(request, "Erro ao criar demanda no banco de dados")
        return RedirectResponse("/noivo/demandas/nova", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/noivo/demandas/{id_demanda}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/demandas")
async def visualizar_demanda(
    request: Request, id_demanda: int, usuario_logado: dict = {}
):
    """Visualiza detalhes de uma demanda com seus itens"""
    from core.repositories import item_demanda_repo, orcamento_repo

    id_noivo = usuario_logado["id"]
    logger.info("Visualizando demanda", noivo_id=id_noivo, demanda_id=id_demanda)

    # Buscar demanda
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada", demanda_id=id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    # Verificar se a demanda pertence ao casal do noivo
    if not casal or demanda.id_casal != casal.id:
        logger.warning(
            "Acesso negado à demanda",
            demanda_id=id_demanda,
            noivo_id=id_noivo,
            demanda_casal_id=demanda.id_casal,
            casal_id=casal.id if casal else None,
        )
        informar_erro(request, "Acesso negado")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar itens da demanda
    itens_demanda = item_demanda_repo.obter_por_demanda(id_demanda)

    # Enriquecer itens com informações de orçamentos
    itens_enriched = []
    for item in itens_demanda:
        # Contar quantos item_orcamento existem para este item_demanda
        total_orcamentos = item_orcamento_repo.contar_por_item_demanda(item["id"])

        # Verificar se o item está atendido (tem item_orcamento aceito)
        esta_atendido = item_orcamento_repo.verificar_item_demanda_ja_aceito(item["id"])

        item_dict = dict(item)
        item_dict["total_orcamentos"] = total_orcamentos
        item_dict["esta_atendido"] = esta_atendido
        itens_enriched.append(item_dict)

    # Buscar orçamentos da demanda
    orcamentos = orcamento_repo.obter_por_demanda(id_demanda)

    return templates.TemplateResponse(
        "noivo/demanda_detalhes.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "demanda": demanda,
            "itens": itens_enriched,
            "orcamentos": orcamentos,
        },
    )


@router.post("/noivo/demandas/{id_demanda}/excluir")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/demandas")
async def excluir_demanda(
    request: Request, id_demanda: int, usuario_logado: dict = {}
):
    """Exclui uma demanda e seus itens e orçamentos relacionados"""
    from core.repositories import item_demanda_repo, orcamento_repo, item_orcamento_repo

    id_noivo = usuario_logado["id"]
    logger.info("Excluindo demanda", noivo_id=id_noivo, demanda_id=id_demanda)

    # Buscar demanda
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada para exclusão", demanda_id=id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    # Verificar se a demanda pertence ao casal do noivo
    if not casal or demanda.id_casal != casal.id:
        logger.warning(
            "Acesso negado para excluir demanda",
            demanda_id=id_demanda,
            noivo_id=id_noivo,
        )
        informar_erro(request, "Acesso negado")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar orçamentos da demanda para excluir seus itens
    orcamentos = orcamento_repo.obter_por_demanda(id_demanda)

    # Excluir itens de cada orçamento
    for orcamento in orcamentos:
        item_orcamento_repo.excluir_por_orcamento(orcamento.id)

    # Excluir orçamentos
    for orcamento in orcamentos:
        orcamento_repo.excluir(orcamento.id)

    # Buscar e excluir itens da demanda
    itens = item_demanda_repo.obter_por_demanda(id_demanda)
    for item in itens:
        item_demanda_repo.excluir(item['id'])

    # Excluir a demanda
    demanda_repo.excluir(id_demanda)

    logger.info(
        "Demanda excluída com sucesso",
        demanda_id=id_demanda,
        total_itens=len(itens),
        total_orcamentos=len(orcamentos),
    )

    informar_sucesso(request, "Demanda excluída com sucesso")
    return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/noivo/demandas/editar/{id_demanda}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/demandas")
async def editar_demanda_form(
    request: Request, id_demanda: int, usuario_logado: dict = {}
):
    """Formulário para editar demanda"""
    from core.repositories import item_demanda_repo, categoria_repo

    id_noivo = usuario_logado["id"]
    logger.info("Editando demanda", noivo_id=id_noivo, demanda_id=id_demanda)

    # Buscar demanda
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada para edição", demanda_id=id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    # Verificar se a demanda pertence ao casal do noivo
    if not casal or demanda.id_casal != casal.id:
        logger.warning(
            "Acesso negado para editar demanda",
            demanda_id=id_demanda,
            noivo_id=id_noivo,
        )
        informar_erro(request, "Acesso negado")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se demanda pode ser editada
    if demanda.status.value != 'ATIVA':
        logger.warning(
            "Tentativa de editar demanda não ativa",
            demanda_id=id_demanda,
            status=demanda.status.value,
        )
        informar_erro(request, "Apenas demandas ativas podem ser editadas")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar itens da demanda
    itens_demanda = item_demanda_repo.obter_por_demanda(id_demanda)

    # Buscar categorias agrupadas por tipo
    from core.models.tipo_fornecimento_model import TipoFornecimento
    categorias = categoria_repo.buscar_categorias()
    # Usar chaves SEM acento para compatibilidade com JavaScript normalize()
    categorias_por_tipo = {
        "PRODUTO": [{"id": c.id, "nome": c.nome} for c in categorias if c.ativo and c.tipo_fornecimento == TipoFornecimento.PRODUTO],
        "SERVICO": [{"id": c.id, "nome": c.nome} for c in categorias if c.ativo and c.tipo_fornecimento == TipoFornecimento.SERVICO],
        "ESPACO": [{"id": c.id, "nome": c.nome} for c in categorias if c.ativo and c.tipo_fornecimento == TipoFornecimento.ESPACO],
    }

    return templates.TemplateResponse(
        "noivo/demanda_form.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "editar",
            "demanda": demanda,
            "itens_demanda": itens_demanda,
            "categorias_por_tipo": categorias_por_tipo,
            "casal": casal,
        },
    )


@router.post("/noivo/demandas/editar/{id_demanda}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(template_erro="noivo/demanda_form.html")
async def atualizar_demanda(
    request: Request,
    id_demanda: int,
    descricao: str = Form(...),
    orcamento_total: str = Form(""),
    data_casamento: str = Form(""),
    cidade_casamento: str = Form(""),
    prazo_entrega: str = Form(""),
    observacoes: str = Form(""),
    tipo: list = Form([], alias="tipo[]"),
    id_categoria: list = Form([], alias="id_categoria[]"),
    descricao_item: list = Form([], alias="descricao_item[]"),
    quantidade: list = Form([], alias="quantidade[]"),
    preco_maximo: list = Form([], alias="preco_maximo[]"),
    observacoes_item: list = Form([], alias="observacoes_item[]"),
    usuario_logado: dict = {},
):
    """Atualiza uma demanda existente com itens (descrições livres)"""
    from core.repositories import item_demanda_repo
    from core.models.item_demanda_model import ItemDemanda

    id_noivo = usuario_logado["id"]
    logger.info("Atualizando demanda", noivo_id=id_noivo, demanda_id=id_demanda)

    # Buscar demanda
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada para atualização", demanda_id=id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar casal do noivo
    casal = casal_repo.obter_por_noivo(id_noivo)

    # Verificar permissão
    if not casal or demanda.id_casal != casal.id:
        logger.warning("Acesso negado para atualizar demanda", demanda_id=id_demanda)
        informar_erro(request, "Acesso negado")
        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Validar que pelo menos um item foi fornecido
    if not tipo or len(tipo) == 0:
        logger.warning("Tentativa de atualizar demanda sem itens", demanda_id=id_demanda)
        informar_erro(request, "Adicione pelo menos um item à demanda")
        return RedirectResponse(f"/noivo/demandas/editar/{id_demanda}", status_code=status.HTTP_303_SEE_OTHER)

    # Converter orcamento_total de string para float
    orcamento_total_valor = None
    if orcamento_total and orcamento_total.strip():
        try:
            orcamento_total_valor = float(orcamento_total)
        except (ValueError, TypeError):
            logger.warning("Valor de orçamento total inválido na atualização", valor=orcamento_total)

    # Atualizar dados da demanda
    demanda.descricao = descricao
    demanda.orcamento_total = orcamento_total_valor
    demanda.data_casamento = data_casamento if data_casamento else casal.data_casamento
    demanda.cidade_casamento = cidade_casamento if cidade_casamento else casal.local_previsto
    demanda.prazo_entrega = prazo_entrega if prazo_entrega else None
    demanda.observacoes = observacoes if observacoes else None

    # Atualizar demanda no banco
    sucesso = demanda_repo.atualizar(demanda)

    if sucesso:
        # Excluir itens antigos
        item_demanda_repo.excluir_por_demanda(id_demanda)

        # Inserir novos itens (descrições livres)
        itens_inseridos = 0
        for i in range(len(tipo)):
            try:
                tipo_valor = tipo[i] if i < len(tipo) else None
                id_cat = int(id_categoria[i]) if i < len(id_categoria) and id_categoria[i] else None
                desc_item = descricao_item[i] if i < len(descricao_item) else None
                qtd = int(quantidade[i]) if i < len(quantidade) and quantidade[i] else 1
                preco_max = float(preco_maximo[i]) if i < len(preco_maximo) and preco_maximo[i] else None
                obs_item = observacoes_item[i] if i < len(observacoes_item) and observacoes_item[i] else None

                if tipo_valor and id_cat and desc_item:
                    item_demanda = ItemDemanda(
                        id=0,  # Será definido pelo banco
                        id_demanda=id_demanda,
                        tipo=tipo_valor,
                        id_categoria=id_cat,
                        descricao=desc_item,
                        quantidade=qtd,
                        preco_maximo=preco_max,
                        observacoes=obs_item
                    )
                    item_demanda_repo.inserir(item_demanda)
                    itens_inseridos += 1
            except Exception as e:
                logger.error("Erro ao inserir item da demanda", erro=e, demanda_id=id_demanda, item_index=i)

        logger.info(
            "Demanda atualizada com sucesso",
            demanda_id=id_demanda,
            total_itens=itens_inseridos
        )
        informar_sucesso(request, f"Demanda atualizada com sucesso! {itens_inseridos} itens salvos.")
        return RedirectResponse(
            f"/noivo/demandas/{id_demanda}", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        logger.error("Falha ao atualizar demanda no banco", demanda_id=id_demanda)
        informar_erro(request, "Erro ao atualizar demanda no banco de dados")
        return RedirectResponse(f"/noivo/demandas/editar/{id_demanda}", status_code=status.HTTP_303_SEE_OTHER)


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
                "demanda_descricao": (
                    demanda_data.descricao if demanda_data else "Demanda não encontrada"
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
    fornecedor = fornecedor_repo.obter_por_id(orcamento.id_fornecedor_prestador)

    # Buscar itens do orçamento (query já faz JOIN com item, traz nome, descricao, tipo)
    itens_orcamento = item_orcamento_repo.obter_por_orcamento(orcamento.id)

    # Enriquecer itens com dados do item (dados já vêm da query via JOIN)
    itens_enriched = []
    for item_orc in itens_orcamento:
        item_dict = {
            "id_item_orcamento": item_orc["id"],  # ID do item_orcamento (necessário para aceitar/rejeitar)
            "id_item": item_orc["id_item"],
            "nome_item": item_orc.get("item_nome", "Item não encontrado"),
            "descricao_item": item_orc.get("item_descricao", ""),
            "tipo_item": item_orc.get("item_tipo", ""),
            "quantidade": item_orc["quantidade"],
            "preco_unitario": item_orc["preco_unitario"],
            "desconto": item_orc.get("desconto", 0) or 0,
            "preco_total": item_orc["preco_total"],
            "observacoes": item_orc.get("observacoes"),
            "status": item_orc.get("status", "PENDENTE"),
        }
        itens_enriched.append(item_dict)

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


# ==================== ROTAS ANTIGAS (DEPRECATED) ====================
# NOTA: As rotas abaixo são da versão antiga (V2) onde o orçamento inteiro
# era aceito/rejeitado de uma vez. Na V3, trabalhamos com status POR ITEM.
# Essas rotas foram REMOVIDAS pois conflitam com o novo modelo de negócio.
# Use as rotas /item/{id}/aceitar e /item/{id}/rejeitar para aceitar/rejeitar
# itens individualmente.


@router.post("/noivo/orcamentos/{id_orcamento}/item/{id_item_orcamento}/aceitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/orcamentos")
async def aceitar_item_orcamento(
    request: Request,
    id_orcamento: int,
    id_item_orcamento: int,
    usuario_logado: dict = {},
):
    """Aceita um item individual do orçamento (POST para segurança CSRF)"""
    logger.info(
        "Aceitando item de orçamento",
        noivo_id=usuario_logado["id"],
        orcamento_id=id_orcamento,
        item_orcamento_id=id_item_orcamento,
    )

    from core.repositories.item_orcamento_repo import item_orcamento_repo

    # Buscar o item do orçamento
    item_orcamento = item_orcamento_repo.obter_por_id(id_item_orcamento)
    if not item_orcamento:
        logger.warning(
            "Item de orçamento não encontrado", item_orcamento_id=id_item_orcamento
        )
        informar_erro(request, "Item de orçamento não encontrado!")
        return RedirectResponse(
            f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se o item pertence ao orçamento correto
    if item_orcamento.id_orcamento != id_orcamento:
        logger.warning(
            "Item não pertence ao orçamento",
            item_orcamento_id=id_item_orcamento,
            orcamento_esperado=id_orcamento,
            orcamento_real=item_orcamento.id_orcamento,
        )
        informar_erro(request, "Item não pertence a este orçamento!")
        return RedirectResponse(
            f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se já existe um item aceito para o mesmo item_demanda
    # REGRA: Não pode aceitar dois orçamentos para o mesmo item_demanda
    if item_orcamento_repo.verificar_item_demanda_ja_aceito(
        item_orcamento.id_item_demanda
    ):
        logger.warning(
            "Já existe item aceito para este item_demanda",
            item_demanda_id=item_orcamento.id_item_demanda,
        )
        informar_erro(
            request,
            "Já existe um item aceito para esta solicitação! "
            "Você não pode aceitar dois orçamentos para o mesmo item.",
        )
        return RedirectResponse(
            f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
        )

    # Aceitar o item
    sucesso = item_orcamento_repo.atualizar_status_item(id_item_orcamento, "ACEITO")

    if sucesso:
        logger.info(
            "Item de orçamento aceito com sucesso",
            item_orcamento_id=id_item_orcamento,
            orcamento_id=id_orcamento,
        )

        # Atualizar status derivado do orçamento
        orcamento_repo.atualizar_status_derivado(id_orcamento)

        # Atualizar valor total do orçamento (soma apenas itens aceitos)
        valor_total = item_orcamento_repo.obter_total_orcamento(id_orcamento)
        orcamento_repo.atualizar_valor_total(id_orcamento, valor_total)

        informar_sucesso(request, "Item aceito com sucesso!")
    else:
        logger.error(
            "Falha ao aceitar item de orçamento",
            item_orcamento_id=id_item_orcamento,
            orcamento_id=id_orcamento,
        )
        informar_erro(request, "Erro ao aceitar item!")

    return RedirectResponse(
        f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/noivo/orcamentos/{id_orcamento}/item/{id_item_orcamento}/rejeitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
@tratar_erro_rota(redirect_erro="/noivo/orcamentos")
async def rejeitar_item_orcamento(
    request: Request,
    id_orcamento: int,
    id_item_orcamento: int,
    motivo_rejeicao: str = Form(""),
    usuario_logado: dict = {},
):
    """Rejeita um item individual do orçamento com motivo opcional"""
    logger.info(
        "Rejeitando item de orçamento",
        noivo_id=usuario_logado["id"],
        orcamento_id=id_orcamento,
        item_orcamento_id=id_item_orcamento,
        motivo=motivo_rejeicao or "Não informado",
    )

    from core.repositories.item_orcamento_repo import item_orcamento_repo

    # Buscar o item do orçamento
    item_orcamento = item_orcamento_repo.obter_por_id(id_item_orcamento)
    if not item_orcamento:
        logger.warning(
            "Item de orçamento não encontrado", item_orcamento_id=id_item_orcamento
        )
        informar_erro(request, "Item de orçamento não encontrado!")
        return RedirectResponse(
            f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
        )

    # Verificar se o item pertence ao orçamento correto
    if item_orcamento.id_orcamento != id_orcamento:
        logger.warning(
            "Item não pertence ao orçamento",
            item_orcamento_id=id_item_orcamento,
            orcamento_esperado=id_orcamento,
            orcamento_real=item_orcamento.id_orcamento,
        )
        informar_erro(request, "Item não pertence a este orçamento!")
        return RedirectResponse(
            f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
        )

    # Rejeitar o item com motivo (se fornecido)
    motivo = motivo_rejeicao.strip() if motivo_rejeicao else None
    sucesso = item_orcamento_repo.atualizar_status_item(
        id_item_orcamento, "REJEITADO", motivo
    )

    if sucesso:
        logger.info(
            "Item de orçamento rejeitado com sucesso",
            item_orcamento_id=id_item_orcamento,
            orcamento_id=id_orcamento,
        )

        # Atualizar status derivado do orçamento
        orcamento_repo.atualizar_status_derivado(id_orcamento)

        # Atualizar valor total do orçamento (soma apenas itens aceitos)
        valor_total = item_orcamento_repo.obter_total_orcamento(id_orcamento)
        orcamento_repo.atualizar_valor_total(id_orcamento, valor_total)

        informar_sucesso(request, "Item rejeitado com sucesso!")
    else:
        logger.error(
            "Falha ao rejeitar item de orçamento",
            item_orcamento_id=id_item_orcamento,
            orcamento_id=id_orcamento,
        )
        informar_erro(request, "Erro ao rejeitar item!")

    return RedirectResponse(
        f"/noivo/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER
    )


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


# ==================== API ENDPOINTS (AJAX) ====================
# Removido: /api/itens/categoria/{id_categoria}
# Não é mais necessário - ItemDemanda agora usa descrições livres, não itens do catálogo
