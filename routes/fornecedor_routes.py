from fastapi import APIRouter, Request, Form, status, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from core.models.demanda_model import StatusDemanda
from infrastructure.security import requer_autenticacao
from util.error_handlers import tratar_erro_rota
from infrastructure.logging import logger
from core.models.usuario_model import TipoUsuario
from core.models.item_model import Item
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories import (
    fornecedor_repo,
    item_repo,
    orcamento_repo,
    demanda_repo,
    usuario_repo,
    categoria_repo,
    casal_repo,
    item_orcamento_repo,
)
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso
from util.template_helpers import template_response_with_flash, configurar_filtros_jinja
from util.item_foto_util import excluir_foto_item
from util.route_helpers import get_active_page
from decimal import Decimal

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)


def get_fornecedor_active_page(request: Request) -> str:
    """
    Determina qual página está ativa na área fornecedor.
    DEPRECATED: Usa get_active_page do route_helpers.
    Mantido para compatibilidade.
    """
    return get_active_page(request, "fornecedor")


# ==================== DASHBOARD ====================


@router.get("/fornecedor")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def root_fornecedor(request: Request, usuario_logado: dict = {}):
    return RedirectResponse("/fornecedor/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/fornecedor/dashboard")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/dashboard.html")
async def dashboard_fornecedor(request: Request, usuario_logado: dict = {}):
    """Dashboard principal do fornecedor"""
    from core.repositories import item_demanda_repo

    id_fornecedor = usuario_logado["id"]

    # Buscar dados do fornecedor
    fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)

    # Estatísticas dos itens do fornecedor
    total_itens = item_repo.contar_por_fornecedor(id_fornecedor)
    meus_itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

    # Separar por tipo
    produtos = [item for item in meus_itens if item.tipo == TipoFornecimento.PRODUTO]
    servicos = [item for item in meus_itens if item.tipo == TipoFornecimento.SERVICO]
    espacos = [item for item in meus_itens if item.tipo == TipoFornecimento.ESPACO]

    # Buscar orçamentos do fornecedor
    try:
        orcamentos_fornecedor = orcamento_repo.obter_por_fornecedor_prestador(id_fornecedor)
        orcamentos_pendentes = [o for o in orcamentos_fornecedor if o.status == "PENDENTE"]
        orcamentos_aceitos = [o for o in orcamentos_fornecedor if o.status == "ACEITO"]
    except Exception as e:
        logger.warning("Erro ao buscar orçamentos do fornecedor", erro=e, fornecedor_id=id_fornecedor)
        orcamentos_fornecedor = []
        orcamentos_pendentes = []
        orcamentos_aceitos = []

    # Contar demandas compatíveis
    total_demandas = 0
    try:
        # Buscar categorias que o fornecedor oferece
        categorias_fornecedor = item_repo.obter_categorias_do_fornecedor(id_fornecedor)

        if categorias_fornecedor:
            # Buscar todas as demandas ativas
            demandas_ativas = demanda_repo.obter_por_status(StatusDemanda.ATIVA.value)

            # Filtrar demandas que têm itens compatíveis
            for demanda in demandas_ativas:
                itens_demanda = item_demanda_repo.obter_por_demanda(demanda.id)
                # Verificar se algum item da demanda pertence às categorias do fornecedor
                itens_compativeis = [
                    item for item in itens_demanda if item.get("id_categoria") in categorias_fornecedor
                ]
                if itens_compativeis:
                    total_demandas += 1
    except Exception as e:
        logger.warning("Erro ao contar demandas compatíveis", erro=e, fornecedor_id=id_fornecedor)
        total_demandas = 0

    stats = {
        "total_itens": total_itens,
        "total_produtos": len(produtos),
        "total_servicos": len(servicos),
        "total_espacos": len(espacos),
        "status_verificacao": fornecedor.verificado if fornecedor else False,
        "total_orcamentos": len(orcamentos_fornecedor),
        "orcamentos_pendentes": len(orcamentos_pendentes),
        "orcamentos_aceitos": len(orcamentos_aceitos),
        "total_demandas": total_demandas,
    }

    logger.info(
        "Dashboard fornecedor carregado",
        fornecedor_id=id_fornecedor,
        total_itens=total_itens,
        total_demandas=total_demandas,
    )

    return template_response_with_flash(
        templates,
        "fornecedor/dashboard.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor,
            "stats": stats,
            "itens_recentes": meus_itens[:5],
        },
    )


# ==================== GESTÃO DE ITENS ====================


@router.get("/fornecedor/itens")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/itens.html")
async def listar_itens(request: Request, usuario_logado: dict = {}):
    """Lista todos os itens do fornecedor"""
    id_fornecedor = usuario_logado["id"]
    meus_itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

    # Obter parâmetros de filtro
    search = request.query_params.get("search", "").strip()
    tipo_filter = request.query_params.get("tipo", "")
    status_filter = request.query_params.get("status", "")
    preco_max = request.query_params.get("preco_max", "")

    # Aplicar filtros
    itens_filtrados = meus_itens

    # Filtro por busca (nome ou descrição)
    if search:
        itens_filtrados = [
            item
            for item in itens_filtrados
            if search.lower() in item.nome.lower() or search.lower() in item.descricao.lower()
        ]

    # Filtro por tipo
    if tipo_filter:
        itens_filtrados = [item for item in itens_filtrados if item.tipo.value.lower() == tipo_filter.lower()]

    # Filtro por status
    if status_filter:
        if status_filter == "ativo":
            itens_filtrados = [item for item in itens_filtrados if item.ativo]
        elif status_filter == "inativo":
            itens_filtrados = [item for item in itens_filtrados if not item.ativo]

    # Filtro por preço máximo
    if preco_max:
        try:
            preco_max_valor = float(preco_max)
            itens_filtrados = [item for item in itens_filtrados if item.preco <= preco_max_valor]
        except ValueError:
            logger.warning("Valor de preço máximo inválido", preco_max=preco_max)

    logger.info("Itens listados", fornecedor_id=id_fornecedor, total=len(itens_filtrados))

    return templates.TemplateResponse(
        "fornecedor/itens.html", {"request": request, "usuario_logado": usuario_logado, "itens": itens_filtrados}
    )


@router.get("/fornecedor/itens/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def novo_item_form(request: Request, usuario_logado: dict = {}):
    """Formulário para criar novo item"""
    categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
    return templates.TemplateResponse(
        "fornecedor/item_form.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias,
        },
    )


@router.post("/fornecedor/itens/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/item_form.html")
async def criar_item(
    request: Request,
    tipo: str = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    observacoes: str = Form(""),
    categoria: str = Form(...),
    foto: UploadFile = File(None),
    usuario_logado: dict = {},
):
    """Cria um novo item"""
    id_fornecedor = usuario_logado["id"]

    # Validar tipo
    try:
        tipo_enum = TipoFornecimento(tipo)
    except ValueError:
        logger.warning("Tipo de item inválido", tipo=tipo, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Tipo de item inválido",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    # Validar categoria
    if not categoria:
        logger.warning("Categoria não fornecida", fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria é obrigatória",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    try:
        categoria_id = int(categoria)
    except ValueError:
        logger.warning("Categoria inválida", categoria=categoria, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria inválida",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    # Validar se categoria pertence ao tipo
    categoria_obj = categoria_repo.obter_por_id(categoria_id)
    if not categoria_obj or categoria_obj.tipo_fornecimento != tipo_enum:
        logger.warning(
            "Categoria não pertence ao tipo", tipo=tipo, categoria_id=categoria_id, fornecedor_id=id_fornecedor
        )
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": f"A categoria selecionada não pertence ao tipo {tipo_enum.value}",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    # Criar item
    novo_item = Item(
        id=0,
        id_fornecedor=id_fornecedor,
        tipo=tipo_enum,
        nome=nome,
        descricao=descricao,
        preco=Decimal(str(preco)),
        observacoes=observacoes if observacoes else None,
        ativo=True,
        data_cadastro=None,
        id_categoria=categoria_id,
    )

    item_id = item_repo.inserir(novo_item)

    if item_id:
        # Processar foto se fornecida
        if foto and foto.filename:
            from util.image_processor import ImageProcessor
            from util.file_storage import FileStorageManager, TipoArquivo
            from config.constants import ImageConstants

            # Criar diretório se não existir
            FileStorageManager.criar_diretorio(TipoArquivo.ITEM)

            # Obter caminho físico para salvar
            caminho_arquivo = FileStorageManager.obter_caminho(TipoArquivo.ITEM, item_id, fisico=True)

            # Processar e salvar usando ImageProcessor
            sucesso, erro = await ImageProcessor.processar_e_salvar_imagem(
                foto, caminho_arquivo, tamanho=ImageConstants.Sizes.ITEM.value  # (600, 600)
            )

            if sucesso:
                logger.info("Item criado com foto", item_id=item_id, fornecedor_id=id_fornecedor, nome=nome)
                informar_sucesso(request, "Item criado com sucesso e foto adicionada!")
            else:
                logger.warning("Erro ao salvar foto do item", item_id=item_id, erro=erro)
                informar_sucesso(request, f"Item criado com sucesso! Foto não salva: {erro}")
        else:
            logger.info("Item criado sem foto", item_id=item_id, fornecedor_id=id_fornecedor, nome=nome)
            informar_sucesso(request, "Item criado com sucesso!")

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    else:
        logger.error("Erro ao inserir item no banco", fornecedor_id=id_fornecedor, nome=nome)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao criar item",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )


@router.get("/fornecedor/itens/{id_item}/editar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def editar_item_form(request: Request, id_item: int, usuario_logado: dict = {}):
    """Formulário para editar item"""
    id_fornecedor = usuario_logado["id"]
    item = item_repo.obter_por_id(id_item)

    if not item or item.id_fornecedor != id_fornecedor:
        logger.warning("Tentativa de editar item não autorizado", item_id=id_item, fornecedor_id=id_fornecedor)
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
    logger.info("Formulário de edição carregado", item_id=id_item, fornecedor_id=id_fornecedor)
    return templates.TemplateResponse(
        "fornecedor/item_form.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "editar",
            "item": item,
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias,
        },
    )


@router.post("/fornecedor/itens/{id_item}/editar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def atualizar_item(
    request: Request,
    id_item: int,
    tipo: str = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    observacoes: str = Form(""),
    categoria: str = Form(...),
    ativo: bool = Form(True),
    usuario_logado: dict = {},
):
    """Atualiza um item existente"""
    id_fornecedor = usuario_logado["id"]

    # Verificar se o item pertence ao fornecedor
    item_existente = item_repo.obter_por_id(id_item)
    if not item_existente or item_existente.id_fornecedor != id_fornecedor:
        logger.warning("Tentativa de atualizar item não autorizado", item_id=id_item, fornecedor_id=id_fornecedor)
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    # Validar tipo
    try:
        tipo_enum = TipoFornecimento(tipo)
    except ValueError:
        logger.warning("Tipo de item inválido ao atualizar", tipo=tipo, item_id=id_item)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Tipo de item inválido",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    # Validar categoria
    if not categoria:
        logger.warning("Categoria não fornecida ao atualizar", item_id=id_item)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria é obrigatória",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    try:
        categoria_id = int(categoria)
    except ValueError:
        logger.warning("Categoria inválida ao atualizar", categoria=categoria, item_id=id_item)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria inválida",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    # Validar se categoria pertence ao tipo
    categoria_obj_validacao = categoria_repo.obter_por_id(categoria_id)
    if not categoria_obj_validacao or categoria_obj_validacao.tipo_fornecimento != tipo_enum:
        logger.warning(
            "Categoria não pertence ao tipo ao atualizar", tipo=tipo, categoria_id=categoria_id, item_id=id_item
        )
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": f"A categoria selecionada não pertence ao tipo {tipo_enum.value}",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )

    # Atualizar item
    item_atualizado = Item(
        id=id_item,
        id_fornecedor=id_fornecedor,
        tipo=tipo_enum,
        nome=nome,
        descricao=descricao,
        preco=Decimal(str(preco)),
        observacoes=observacoes if observacoes else None,
        ativo=ativo,
        data_cadastro=item_existente.data_cadastro,
        id_categoria=categoria_id,
    )

    sucesso = item_repo.atualizar(item_atualizado)

    if sucesso:
        logger.info("Item atualizado com sucesso", item_id=id_item, fornecedor_id=id_fornecedor, nome=nome)
        informar_sucesso(request, "Item atualizado com sucesso!")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    else:
        logger.error("Erro ao atualizar item no banco", item_id=id_item, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse(
            "fornecedor/item_form.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao atualizar item",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoFornecimento],
                "categorias": categorias,
            },
        )


@router.post("/fornecedor/itens/{id_item}/excluir")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def excluir_item(request: Request, id_item: int, confirmar: str = Form(None), usuario_logado: dict = {}):
    """Exclui um item"""
    id_fornecedor = usuario_logado["id"]
    sucesso = item_repo.excluir_item_fornecedor(id_item, id_fornecedor)

    if sucesso:
        logger.info("Item excluído com sucesso", item_id=id_item, fornecedor_id=id_fornecedor)
        informar_sucesso(request, "Item excluído com sucesso!")
    else:
        logger.error("Erro ao excluir item", item_id=id_item, fornecedor_id=id_fornecedor)
        informar_erro(request, "Erro ao excluir item!")

    return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/fornecedor/itens/{id_item}/ativar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def ativar_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Ativa um item"""
    id_fornecedor = usuario_logado["id"]
    sucesso = item_repo.ativar_item(id_item, id_fornecedor)

    if sucesso:
        logger.info("Item ativado com sucesso", item_id=id_item, fornecedor_id=id_fornecedor)
        informar_sucesso(request, "Item ativado com sucesso!")
    else:
        logger.error("Erro ao ativar item", item_id=id_item, fornecedor_id=id_fornecedor)
        informar_erro(request, "Erro ao ativar item!")

    return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/fornecedor/itens/{id_item}/desativar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def desativar_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Desativa um item"""
    id_fornecedor = usuario_logado["id"]
    sucesso = item_repo.desativar_item(id_item, id_fornecedor)

    if sucesso:
        logger.info("Item desativado com sucesso", item_id=id_item, fornecedor_id=id_fornecedor)
        informar_sucesso(request, "Item desativado com sucesso!")
    else:
        logger.error("Erro ao desativar item", item_id=id_item, fornecedor_id=id_fornecedor)
        informar_erro(request, "Erro ao desativar item!")

    return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)


# ==================== ORÇAMENTOS ====================


@router.get("/fornecedor/orcamentos")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/orcamentos.html")
async def listar_orcamentos(request: Request, status_filter: str = "", usuario_logado: dict = {}):
    """Lista orçamentos do fornecedor"""
    id_fornecedor = usuario_logado["id"]

    # Buscar orçamentos do fornecedor
    orcamentos = orcamento_repo.obter_por_fornecedor_prestador(id_fornecedor)

    # Filtrar por status se especificado
    if status_filter:
        orcamentos = [o for o in orcamentos if o.status.upper() == status_filter.upper()]

    # Enriquecer dados dos orçamentos
    orcamentos_enriched = []
    for orcamento in orcamentos:
        try:
            # Buscar dados da demanda
            demanda = demanda_repo.obter_por_id(orcamento.id_demanda)

            # Buscar dados do casal e noivos
            noivos_nomes = "Casal não identificado"
            if demanda:
                try:
                    casal = casal_repo.obter_por_id(demanda.id_casal)
                    if casal:
                        noivo1 = usuario_repo.obter_por_id(casal.id_noivo1)
                        noivo2 = usuario_repo.obter_por_id(casal.id_noivo2) if casal.id_noivo2 else None

                        if noivo1 and noivo2:
                            noivos_nomes = f"{noivo1.nome} & {noivo2.nome}"
                        elif noivo1:
                            noivos_nomes = noivo1.nome
                except Exception as e_noivos:
                    logger.warning("Erro ao buscar noivos", erro=e_noivos, demanda_id=demanda.id)

            # Buscar itens do orçamento para contar
            itens = item_orcamento_repo.obter_por_orcamento(orcamento.id)
            orcamento.itens_count = len(itens)

            # Adicionar data_envio (usar data_hora_cadastro)
            if orcamento.data_hora_cadastro:
                if isinstance(orcamento.data_hora_cadastro, str):
                    from datetime import datetime

                    dt = datetime.fromisoformat(orcamento.data_hora_cadastro)
                    orcamento.data_envio = dt.strftime("%d/%m/%Y %H:%M")
                else:
                    orcamento.data_envio = orcamento.data_hora_cadastro.strftime("%d/%m/%Y %H:%M")
            else:
                orcamento.data_envio = None

            # Adicionar título da demanda e nomes dos noivos
            orcamento.demanda_titulo = demanda.descricao if demanda else "Demanda sem título"
            orcamento.noivos_nomes = noivos_nomes

            # Log para debug
            logger.info(
                "Orçamento enriquecido",
                orcamento_id=orcamento.id,
                noivos_nomes=getattr(orcamento, 'noivos_nomes', 'ATRIBUTO NÃO ENCONTRADO'),
                demanda_titulo=getattr(orcamento, 'demanda_titulo', 'ATRIBUTO NÃO ENCONTRADO'),
            )

            orcamentos_enriched.append(orcamento)
        except Exception as e:
            logger.error("Erro ao enriquecer orçamento", erro=e, orcamento_id=orcamento.id)
            # Adicionar mesmo com dados incompletos
            orcamento.itens_count = 0
            orcamento.data_envio = None
            orcamento.demanda_titulo = "Demanda sem título"
            orcamento.noivos_nomes = "Casal não identificado"
            orcamentos_enriched.append(orcamento)

    logger.info("Orçamentos listados", fornecedor_id=id_fornecedor, total=len(orcamentos_enriched))
    return templates.TemplateResponse(
        "fornecedor/orcamentos.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamentos": orcamentos_enriched,
            "status_filter": status_filter,
        },
    )


@router.get("/fornecedor/orcamentos/{id_orcamento}")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/orcamentos")
async def visualizar_orcamento_fornecedor(request: Request, id_orcamento: int, usuario_logado: dict = {}):
    """Visualiza detalhes de um orçamento enviado pelo fornecedor"""
    id_fornecedor = usuario_logado["id"]
    logger.info("Fornecedor visualizando orçamento", fornecedor_id=id_fornecedor, orcamento_id=id_orcamento)

    # Buscar orçamento
    orcamento = orcamento_repo.obter_por_id(id_orcamento)
    if not orcamento:
        logger.warning("Orçamento não encontrado", orcamento_id=id_orcamento)
        informar_erro(request, "Orçamento não encontrado")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se o orçamento pertence ao fornecedor logado
    if orcamento.id_fornecedor_prestador != id_fornecedor:
        logger.warning("Acesso negado ao orçamento", orcamento_id=id_orcamento, fornecedor_id=id_fornecedor)
        informar_erro(request, "Você não tem permissão para visualizar este orçamento")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar demanda relacionada
    demanda = demanda_repo.obter_por_id(orcamento.id_demanda)

    # Buscar noivo (dono da demanda)
    noivo = None
    if demanda:
        casal = casal_repo.obter_por_id(demanda.id_casal)
        if casal:
            noivo = usuario_repo.obter_por_id(casal.id_noivo1)

    # Buscar itens do orçamento com detalhes
    itens_orcamento = item_orcamento_repo.obter_por_orcamento(orcamento.id)

    # Enriquecer itens com dados
    itens_enriched = []
    for item_orc in itens_orcamento:
        item_dict = {
            "id": item_orc.get("id"),
            "id_item": item_orc["id_item"],
            "id_item_demanda": item_orc.get("id_item_demanda"),
            "nome_item": item_orc.get("item_nome", "Item não encontrado"),
            "descricao_item_demanda": item_orc.get("item_demanda_descricao", ""),
            "categoria": item_orc.get("categoria_nome", ""),
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
        "status": orcamento.status,
        "valor_total": orcamento.valor_total,
        "data_envio": orcamento.data_hora_cadastro,
        "data_validade": orcamento.data_hora_validade,
        "observacoes": orcamento.observacoes,
        "itens": itens_enriched,
        "total_itens": len(itens_enriched),
    }

    return templates.TemplateResponse(
        "fornecedor/orcamento_detalhes.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamento": orcamento_enriched,
            "demanda": demanda,
            "noivo": noivo,
        },
    )


@router.get("/fornecedor/demandas")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/demandas.html")
async def listar_demandas(request: Request, categoria: str = "", usuario_logado: dict = {}):
    """Lista demandas disponíveis compatíveis com categorias do fornecedor (V2)"""
    from core.repositories import item_demanda_repo, categoria_repo

    id_fornecedor = usuario_logado["id"]

    # Buscar categorias que o fornecedor oferece itens
    categorias_fornecedor = item_repo.obter_categorias_do_fornecedor(id_fornecedor)

    if not categorias_fornecedor:
        logger.info("Fornecedor sem itens cadastrados", fornecedor_id=id_fornecedor)
        return templates.TemplateResponse(
            "fornecedor/demandas.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "demandas": [],
                "categorias": [],
                "categoria_filter": categoria,
                "mensagem": "Cadastre itens para visualizar demandas compatíveis.",
            },
        )

    # Buscar todas as demandas ativas
    demandas = demanda_repo.obter_por_status(StatusDemanda.ATIVA.value)

    # Filtrar demandas que têm itens compatíveis (por tipo+categoria)
    demandas_compativeis = []
    for demanda in demandas:
        # Buscar itens da demanda (com descrições livres)
        itens_demanda = item_demanda_repo.obter_por_demanda(demanda.id)

        # Verificar se algum item da demanda pertence às categorias do fornecedor
        itens_compativeis = [item for item in itens_demanda if item.get("id_categoria") in categorias_fornecedor]

        if itens_compativeis:
            demandas_compativeis.append(
                {"demanda": demanda, "itens_compativeis": itens_compativeis, "total_itens": len(itens_demanda)}
            )

    # Filtrar por categoria se especificado (agora filtra nos itens, não na demanda)
    if categoria:
        try:
            categoria_id = int(categoria)
            demandas_filtradas = []
            for d in demandas_compativeis:
                # Verificar se algum item compatível é da categoria filtrada
                itens = d.get("itens_compativeis") or []
                if any(item.get("id_categoria") == categoria_id for item in itens):  # type: ignore[attr-defined]
                    demandas_filtradas.append(d)
            demandas_compativeis = demandas_filtradas
        except ValueError:
            logger.warning("Categoria inválida no filtro", categoria=categoria)

    # Enriquecer dados das demandas
    demandas_enriched = []
    for dados in demandas_compativeis:
        demanda = dados["demanda"]  # type: ignore[assignment]
        try:
            # Buscar dados do casal e noivo
            casal = casal_repo.obter_por_id(demanda.id_casal)
            noivo = None
            if casal:
                noivo = usuario_repo.obter_por_id(casal.id_noivo1)

            # Verificar se já existe orçamento deste fornecedor para esta demanda
            orcamentos_existentes = orcamento_repo.obter_por_demanda(demanda.id)
            ja_tem_orcamento = any(o.id_fornecedor_prestador == id_fornecedor for o in orcamentos_existentes)

            demanda_data = {
                "demanda": demanda,
                "noivo": noivo,
                "casal": casal,
                "ja_tem_orcamento": ja_tem_orcamento,
                "itens_compativeis": dados["itens_compativeis"],
                "total_itens": dados["total_itens"],
            }
            demandas_enriched.append(demanda_data)
        except Exception as e:
            logger.warning("Erro ao enriquecer demanda", erro=e, demanda_id=demanda.id)
            demandas_enriched.append(
                {
                    "demanda": demanda,
                    "noivo": None,
                    "casal": None,
                    "ja_tem_orcamento": False,
                    "itens_compativeis": dados["itens_compativeis"],
                    "total_itens": dados["total_itens"],
                }
            )

    # Buscar categorias para filtro
    categorias = categoria_repo.buscar_categorias()

    logger.info("Demandas listadas V2", fornecedor_id=id_fornecedor, total=len(demandas_enriched))
    return templates.TemplateResponse(
        "fornecedor/demandas.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "demandas": demandas_enriched,
            "categorias": categorias,
            "categoria_filter": categoria,
        },
    )


# ==================== ORÇAMENTO COM ITENS ====================
#
# NOTA: Rotas simplificadas de orçamento (sem itens) foram REMOVIDAS.
# Use apenas a rota completa /fornecedor/demandas/{id}/orcamento/novo
# que vincula ItemDemanda → Item do catálogo, conforme arquitetura V3.


@router.get("/fornecedor/demandas/{id_demanda}/orcamento/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/demandas")
async def novo_orcamento_com_itens_form(request: Request, id_demanda: int, usuario_logado: dict = {}):
    """Formulário para criar orçamento detalhado com itens (V2)"""
    from core.repositories import item_demanda_repo

    # Buscar a demanda
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada ao criar orçamento", demanda_id=id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/fornecedor/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar itens da demanda
    itens_demanda_todos = item_demanda_repo.obter_por_demanda(id_demanda)

    # Buscar categorias do fornecedor
    categorias_fornecedor = item_repo.obter_categorias_do_fornecedor(usuario_logado["id"])

    # Filtrar apenas itens_demanda compatíveis com as categorias do fornecedor
    itens_demanda = [item for item in itens_demanda_todos if item.get("id_categoria") in categorias_fornecedor]

    # Buscar itens do fornecedor (apenas ativos)
    meus_itens = item_repo.obter_itens_por_fornecedor(usuario_logado["id"])
    meus_itens = [i for i in meus_itens if i.ativo]

    # Buscar casal e noivo
    casal = casal_repo.obter_por_id(demanda.id_casal)
    noivo = None
    if casal:
        noivo = usuario_repo.obter_por_id(casal.id_noivo1)

    logger.info(
        "Formulário de orçamento V2 carregado",
        demanda_id=id_demanda,
        fornecedor_id=usuario_logado["id"],
        itens_compativeis=len(itens_demanda),
    )

    return templates.TemplateResponse(
        "fornecedor/orcamento_form.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "demanda": demanda,
            "itens_demanda": itens_demanda,
            "meus_itens": meus_itens,
            "noivo": noivo,
            "orcamento": None,
        },
    )


@router.post("/fornecedor/demandas/{id_demanda}/orcamento")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/demandas")
async def criar_orcamento_com_itens(
    request: Request,
    id_demanda: int,
    observacoes: str = Form(""),
    id_item_demanda: list[str] = Form(default=[], alias="id_item_demanda[]"),
    id_item: list[str] = Form(default=[], alias="id_item[]"),
    quantidade: list[str] = Form(default=[], alias="quantidade[]"),
    preco_unitario: list[str] = Form(default=[], alias="preco_unitario[]"),
    desconto_item: list[str] = Form(default=[], alias="desconto_item[]"),
    observacoes_item: list[str] = Form(default=[], alias="observacoes_item[]"),
    usuario_logado: dict = {},
):
    """Cria orçamento com itens detalhados (V2 - vinculado a item_demanda)"""
    from datetime import datetime
    from core.models.orcamento_model import Orcamento
    from core.repositories import item_orcamento_repo, item_demanda_repo
    from core.models.item_orcamento_model import ItemOrcamento

    # Log de debug para verificar dados recebidos (IMPORTANTE)
    logger.warning(
        "DEBUG: Dados recebidos no POST de orçamento",
        id_demanda=id_demanda,
        observacoes=observacoes[:50] if observacoes else "",
        id_item_demanda_tipo=type(id_item_demanda).__name__,
        id_item_demanda_len=len(id_item_demanda) if id_item_demanda else 0,
        id_item_tipo=type(id_item).__name__,
        id_item_len=len(id_item) if id_item else 0,
        quantidade_len=len(quantidade) if quantidade else 0,
        preco_unitario_len=len(preco_unitario) if preco_unitario else 0,
        id_item_demanda_values=id_item_demanda if id_item_demanda else [],
        id_item_values=id_item if id_item else [],
    )

    # Verificar se a demanda existe
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada ao criar orçamento", demanda_id=id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/fornecedor/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se já existe orçamento
    orcamentos_existentes = orcamento_repo.obter_por_demanda(id_demanda)
    ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

    if ja_tem_orcamento:
        logger.warning(
            "Tentativa de criar orçamento duplicado", demanda_id=id_demanda, fornecedor_id=usuario_logado["id"]
        )
        informar_erro(request, "Você já enviou um orçamento para esta demanda")
        return RedirectResponse("/fornecedor/demandas", status_code=status.HTTP_303_SEE_OTHER)

    # Validar que pelo menos 1 item foi fornecido
    if not id_item or len(id_item) == 0 or not id_item_demanda or len(id_item_demanda) == 0:
        logger.warning(
            "Tentativa de criar orçamento sem itens",
            demanda_id=id_demanda,
            id_item_presente=bool(id_item),
            id_item_len=len(id_item) if id_item else 0,
            id_item_demanda_presente=bool(id_item_demanda),
            id_item_demanda_len=len(id_item_demanda) if id_item_demanda else 0,
        )
        informar_erro(request, "Adicione pelo menos um item ao orçamento")
        return RedirectResponse(
            f"/fornecedor/demandas/{id_demanda}/orcamento/novo", status_code=status.HTTP_303_SEE_OTHER
        )

    # Filtrar itens vazios (quando select não foi preenchido)
    indices_validos = []
    for i in range(len(id_item)):
        if id_item[i] and id_item[i] != "" and id_item_demanda[i] and id_item_demanda[i] != "":
            indices_validos.append(i)

    if len(indices_validos) == 0:
        logger.warning("Nenhum item válido encontrado após filtragem", demanda_id=id_demanda)
        informar_erro(request, "Selecione pelo menos um item do catálogo")
        return RedirectResponse(
            f"/fornecedor/demandas/{id_demanda}/orcamento/novo", status_code=status.HTTP_303_SEE_OTHER
        )

    # Validar quantidade de arrays
    if len(id_item) != len(id_item_demanda):
        logger.error("Quantidade de id_item diferente de id_item_demanda")
        informar_erro(request, "Erro nos dados do formulário")
        return RedirectResponse(
            f"/fornecedor/demandas/{id_demanda}/orcamento/novo", status_code=status.HTTP_303_SEE_OTHER
        )

    # Calcular valor total (apenas itens válidos)
    valor_total = 0.0
    for i in indices_validos:
        try:
            qtd = int(quantidade[i]) if i < len(quantidade) else 1
            preco = float(preco_unitario[i]) if i < len(preco_unitario) else 0
            desc_item = float(desconto_item[i]) if i < len(desconto_item) and desconto_item[i] else 0
            subtotal = (qtd * preco) - desc_item
            valor_total += subtotal
        except (ValueError, TypeError):
            pass

    # Criar orçamento
    novo_orcamento = Orcamento(
        id=0,
        id_demanda=id_demanda,
        id_fornecedor_prestador=usuario_logado["id"],
        data_hora_cadastro=datetime.now(),
        data_hora_validade=None,
        status="PENDENTE",
        observacoes=observacoes,
        valor_total=valor_total,
    )

    # Inserir orçamento no banco
    id_orcamento = orcamento_repo.inserir(novo_orcamento)

    if id_orcamento:
        # Inserir itens do orçamento (V2: com id_item_demanda) - apenas itens válidos
        itens_inseridos = 0
        erros_validacao = []

        for i in indices_validos:
            try:
                id_item_demanda_int = int(id_item_demanda[i]) if id_item_demanda[i] else 0
                id_item_int = int(id_item[i]) if id_item[i] else 0
                qtd = int(quantidade[i]) if i < len(quantidade) and quantidade[i] else 1
                preco = float(preco_unitario[i]) if i < len(preco_unitario) and preco_unitario[i] else 0
                desc_item = float(desconto_item[i]) if i < len(desconto_item) and desconto_item[i] else 0.0
                obs_item = observacoes_item[i] if i < len(observacoes_item) and observacoes_item[i] else None

                if id_item_demanda_int == 0 or id_item_int == 0:
                    continue

                # Validar que o item pertence à categoria do item_demanda
                item_obj = item_repo.obter_por_id(id_item_int)
                item_demanda_dict = item_demanda_repo.obter_por_demanda(id_demanda)
                item_demanda_obj = next(
                    (item for item in item_demanda_dict if item.get("id") == id_item_demanda_int), None
                )

                if not item_obj or not item_demanda_obj:
                    erros_validacao.append(f"Item #{id_item_int} ou ItemDemanda #{id_item_demanda_int} não encontrado")
                    continue

                if item_obj.id_categoria != item_demanda_obj.get("id_categoria"):
                    erros_validacao.append(f"Item '{item_obj.nome}' não pertence à categoria do item solicitado")
                    continue

                # Verificar se item já foi usado para este item_demanda
                if item_orcamento_repo.verificar_item_ja_usado(id_orcamento, id_item_demanda_int, id_item_int):
                    erros_validacao.append(f"Item '{item_obj.nome}' já foi adicionado para este item da demanda")
                    continue

                # Criar item_orcamento
                item_orcamento = ItemOrcamento(
                    id=0,  # Será gerado automaticamente
                    id_orcamento=id_orcamento,
                    id_item_demanda=id_item_demanda_int,
                    id_item=id_item_int,
                    quantidade=qtd,
                    preco_unitario=preco,
                    observacoes=obs_item,
                    desconto=desc_item,
                )
                item_orcamento_repo.inserir(item_orcamento)
                itens_inseridos += 1

            except Exception as e:
                logger.error("Erro ao inserir item do orçamento", erro=e, orcamento_id=id_orcamento, item_index=i)
                erros_validacao.append(f"Erro ao processar item #{i+1}: {str(e)}")

        if erros_validacao:
            logger.warning("Orçamento criado com avisos", orcamento_id=id_orcamento, erros=erros_validacao)
            for erro in erros_validacao:
                informar_aviso(request, erro)

        logger.info(
            "Orçamento V2 criado com sucesso",
            orcamento_id=id_orcamento,
            demanda_id=id_demanda,
            fornecedor_id=usuario_logado["id"],
            total_itens=itens_inseridos,
            valor_total=valor_total,
        )

        if itens_inseridos > 0:
            informar_sucesso(request, f"Orçamento enviado com sucesso! {itens_inseridos} item(ns) adicionado(s)")
        else:
            informar_erro(request, "Nenhum item válido foi adicionado ao orçamento")

        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
    else:
        logger.error("Erro ao inserir orçamento no banco", demanda_id=id_demanda, fornecedor_id=usuario_logado["id"])
        informar_erro(request, "Erro ao criar orçamento!")
        return RedirectResponse(
            f"/fornecedor/demandas/{id_demanda}/orcamento/novo", status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/fornecedor/orcamentos/{id_orcamento}/editar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/orcamentos")
async def editar_orcamento_form(request: Request, id_orcamento: int, usuario_logado: dict = {}):
    """Formulário para editar orçamento existente (apenas se PENDENTE)"""
    from core.repositories import item_demanda_repo

    # Buscar o orçamento
    orcamento = orcamento_repo.obter_por_id(id_orcamento)
    if not orcamento:
        logger.warning("Orçamento não encontrado ao editar", orcamento_id=id_orcamento)
        informar_erro(request, "Orçamento não encontrado")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se o orçamento pertence ao fornecedor logado
    if orcamento.id_fornecedor_prestador != usuario_logado["id"]:
        logger.warning(
            "Tentativa de editar orçamento de outro fornecedor",
            orcamento_id=id_orcamento,
            fornecedor_logado=usuario_logado["id"],
            fornecedor_orcamento=orcamento.id_fornecedor_prestador,
        )
        informar_erro(request, "Você não tem permissão para editar este orçamento")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se o orçamento está PENDENTE
    if orcamento.status != "PENDENTE":
        logger.warning(
            "Tentativa de editar orçamento não pendente",
            orcamento_id=id_orcamento,
            status=orcamento.status,
        )
        informar_erro(request, "Apenas orçamentos pendentes podem ser editados")
        return RedirectResponse(f"/fornecedor/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar itens do orçamento
    itens_orcamento = item_orcamento_repo.obter_por_orcamento(id_orcamento)

    # Adicionar id_categoria aos itens (vem como item_id_categoria da query)
    for item in itens_orcamento:
        if "item_id_categoria" in item:
            item["id_categoria"] = item["item_id_categoria"]

    # Buscar a demanda
    demanda = demanda_repo.obter_por_id(orcamento.id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada ao editar orçamento", demanda_id=orcamento.id_demanda)
        informar_erro(request, "Demanda não encontrada")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar itens da demanda
    itens_demanda_todos = item_demanda_repo.obter_por_demanda(orcamento.id_demanda)

    # Buscar categorias do fornecedor
    categorias_fornecedor = item_repo.obter_categorias_do_fornecedor(usuario_logado["id"])

    # Filtrar apenas itens_demanda compatíveis com as categorias do fornecedor
    itens_demanda = [item for item in itens_demanda_todos if item.get("id_categoria") in categorias_fornecedor]

    # Buscar itens do fornecedor (apenas ativos)
    meus_itens = item_repo.obter_itens_por_fornecedor(usuario_logado["id"])
    meus_itens = [i for i in meus_itens if i.ativo]

    # Buscar casal e noivo
    casal = casal_repo.obter_por_id(demanda.id_casal)
    noivo = None
    if casal:
        noivo = usuario_repo.obter_por_id(casal.id_noivo1)

    # Adicionar itens ao objeto orcamento para passar ao template
    orcamento.itens = itens_orcamento

    logger.info(
        "Formulário de edição de orçamento carregado",
        orcamento_id=id_orcamento,
        fornecedor_id=usuario_logado["id"],
        total_itens=len(itens_orcamento),
    )

    return templates.TemplateResponse(
        "fornecedor/orcamento_form.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "demanda": demanda,
            "itens_demanda": itens_demanda,
            "meus_itens": meus_itens,
            "noivo": noivo,
            "orcamento": orcamento,
        },
    )


@router.post("/fornecedor/orcamentos/{id_orcamento}")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/orcamentos")
async def atualizar_orcamento_com_itens(
    request: Request,
    id_orcamento: int,
    observacoes: str = Form(""),
    id_item_demanda: list[str] = Form(default=[], alias="id_item_demanda[]"),
    id_item: list[str] = Form(default=[], alias="id_item[]"),
    quantidade: list[str] = Form(default=[], alias="quantidade[]"),
    preco_unitario: list[str] = Form(default=[], alias="preco_unitario[]"),
    desconto_item: list[str] = Form(default=[], alias="desconto_item[]"),
    observacoes_item: list[str] = Form(default=[], alias="observacoes_item[]"),
    usuario_logado: dict = {},
):
    """Atualiza orçamento existente (apenas se PENDENTE)"""
    from datetime import datetime
    from core.models.orcamento_model import Orcamento
    from core.repositories import item_orcamento_repo, item_demanda_repo
    from core.models.item_orcamento_model import ItemOrcamento

    # Buscar o orçamento
    orcamento = orcamento_repo.obter_por_id(id_orcamento)
    if not orcamento:
        logger.warning("Orçamento não encontrado ao atualizar", orcamento_id=id_orcamento)
        informar_erro(request, "Orçamento não encontrado")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se o orçamento pertence ao fornecedor logado
    if orcamento.id_fornecedor_prestador != usuario_logado["id"]:
        logger.warning(
            "Tentativa de atualizar orçamento de outro fornecedor",
            orcamento_id=id_orcamento,
            fornecedor_logado=usuario_logado["id"],
            fornecedor_orcamento=orcamento.id_fornecedor_prestador,
        )
        informar_erro(request, "Você não tem permissão para editar este orçamento")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se o orçamento está PENDENTE
    if orcamento.status != "PENDENTE":
        logger.warning(
            "Tentativa de atualizar orçamento não pendente",
            orcamento_id=id_orcamento,
            status=orcamento.status,
        )
        informar_erro(request, "Apenas orçamentos pendentes podem ser editados")
        return RedirectResponse(f"/fornecedor/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER)

    # Validar que pelo menos 1 item foi fornecido
    if not id_item or len(id_item) == 0 or not id_item_demanda or len(id_item_demanda) == 0:
        logger.warning(
            "Tentativa de atualizar orçamento sem itens",
            orcamento_id=id_orcamento,
        )
        informar_erro(request, "Adicione pelo menos um item ao orçamento")
        return RedirectResponse(
            f"/fornecedor/orcamentos/{id_orcamento}/editar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Filtrar itens vazios
    indices_validos = []
    for i in range(len(id_item)):
        if id_item[i] and id_item[i] != "" and id_item_demanda[i] and id_item_demanda[i] != "":
            indices_validos.append(i)

    if len(indices_validos) == 0:
        logger.warning("Nenhum item válido encontrado após filtragem", orcamento_id=id_orcamento)
        informar_erro(request, "Selecione pelo menos um item do catálogo")
        return RedirectResponse(
            f"/fornecedor/orcamentos/{id_orcamento}/editar", status_code=status.HTTP_303_SEE_OTHER
        )

    # Calcular valor total (apenas itens válidos)
    valor_total = 0.0
    for i in indices_validos:
        try:
            qtd = int(quantidade[i]) if i < len(quantidade) else 1
            preco = float(preco_unitario[i]) if i < len(preco_unitario) else 0
            desc_item = float(desconto_item[i]) if i < len(desconto_item) and desconto_item[i] else 0.0
            subtotal = (qtd * preco) - desc_item
            valor_total += subtotal
        except (ValueError, TypeError):
            pass

    # Deletar itens existentes do orçamento
    item_orcamento_repo.excluir_por_orcamento(id_orcamento)

    # Inserir novos itens (reutilizando lógica do create)
    itens_inseridos = 0
    erros_validacao = []

    for i in indices_validos:
        try:
            id_item_demanda_int = int(id_item_demanda[i]) if id_item_demanda[i] else 0
            id_item_int = int(id_item[i]) if id_item[i] else 0
            qtd = int(quantidade[i]) if i < len(quantidade) and quantidade[i] else 1
            preco = float(preco_unitario[i]) if i < len(preco_unitario) and preco_unitario[i] else 0
            desc_item = float(desconto_item[i]) if i < len(desconto_item) and desconto_item[i] else 0.0
            obs_item = observacoes_item[i] if i < len(observacoes_item) and observacoes_item[i] else None

            if id_item_demanda_int == 0 or id_item_int == 0:
                continue

            # Validar que o item pertence à categoria do item_demanda
            item_obj = item_repo.obter_por_id(id_item_int)
            item_demanda_dict = item_demanda_repo.obter_por_demanda(orcamento.id_demanda)
            item_demanda_obj = next((item for item in item_demanda_dict if item.get("id") == id_item_demanda_int), None)

            if not item_obj or not item_demanda_obj:
                erros_validacao.append(f"Item #{id_item_int} ou ItemDemanda #{id_item_demanda_int} não encontrado")
                continue

            if item_obj.id_categoria != item_demanda_obj.get("id_categoria"):
                erros_validacao.append(f"Item '{item_obj.nome}' não pertence à categoria do item solicitado")
                continue

            # Criar item_orcamento
            item_orcamento = ItemOrcamento(
                id=0,  # Será gerado automaticamente
                id_orcamento=id_orcamento,
                id_item_demanda=id_item_demanda_int,
                id_item=id_item_int,
                quantidade=qtd,
                preco_unitario=preco,
                observacoes=obs_item,
                desconto=desc_item,
            )
            item_orcamento_repo.inserir(item_orcamento)
            itens_inseridos += 1

        except Exception as e:
            logger.error("Erro ao inserir item do orçamento", erro=e, orcamento_id=id_orcamento, item_index=i)
            erros_validacao.append(f"Erro ao processar item #{i+1}: {str(e)}")

    # Atualizar o orçamento
    orcamento.observacoes = observacoes
    orcamento.valor_total = valor_total
    orcamento_repo.atualizar(orcamento)

    if erros_validacao:
        logger.warning("Orçamento atualizado com avisos", orcamento_id=id_orcamento, erros=erros_validacao)
        for erro in erros_validacao:
            informar_aviso(request, erro)

    logger.info(
        "Orçamento atualizado com sucesso",
        orcamento_id=id_orcamento,
        fornecedor_id=usuario_logado["id"],
        total_itens=itens_inseridos,
        valor_total=valor_total,
    )

    if itens_inseridos > 0:
        informar_sucesso(request, f"Orçamento atualizado com sucesso! {itens_inseridos} item(ns) adicionado(s)")
    else:
        informar_erro(request, "Nenhum item válido foi adicionado ao orçamento")

    return RedirectResponse(f"/fornecedor/orcamentos/{id_orcamento}", status_code=status.HTTP_303_SEE_OTHER)


# ==================== PERFIL ====================


@router.get("/fornecedor/perfil")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/perfil.html")
async def perfil_fornecedor(request: Request, usuario_logado: dict = {}):
    """Página de perfil do fornecedor"""
    id_fornecedor = usuario_logado["id"]
    fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)

    logger.info("Perfil fornecedor carregado", fornecedor_id=id_fornecedor)
    return templates.TemplateResponse(
        "fornecedor/perfil.html", {"request": request, "usuario_logado": usuario_logado, "fornecedor": fornecedor}
    )


@router.post("/fornecedor/perfil")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/perfil.html")
async def atualizar_perfil(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    nome_empresa: str = Form(""),
    cnpj: str = Form(""),
    descricao: str = Form(""),
    newsletter: str = Form(None),
    usuario_logado: dict = {},
):
    """Atualiza perfil do fornecedor"""
    id_fornecedor = usuario_logado["id"]
    fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)

    if not fornecedor:
        logger.error("Fornecedor não encontrado ao atualizar perfil", fornecedor_id=id_fornecedor)
        return templates.TemplateResponse(
            "fornecedor/perfil.html",
            {"request": request, "usuario_logado": usuario_logado, "erro": "Fornecedor não encontrado"},
        )

    # Converter checkboxes para boolean
    newsletter_bool = newsletter == "on"

    # Atualizar dados
    fornecedor.nome = nome
    fornecedor.email = email
    fornecedor.telefone = telefone
    fornecedor.nome_empresa = nome_empresa
    fornecedor.cnpj = cnpj
    fornecedor.descricao = descricao
    fornecedor.newsletter = newsletter_bool

    sucesso = fornecedor_repo.atualizar(fornecedor)

    if sucesso:
        logger.info("Perfil fornecedor atualizado com sucesso", fornecedor_id=id_fornecedor)
        return templates.TemplateResponse(
            "fornecedor/perfil.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "fornecedor": fornecedor,
                "sucesso": "Perfil atualizado com sucesso!",
            },
        )
    else:
        logger.error("Erro ao atualizar perfil no banco", fornecedor_id=id_fornecedor)
        return templates.TemplateResponse(
            "fornecedor/perfil.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "fornecedor": fornecedor,
                "erro": "Erro ao atualizar perfil",
            },
        )


@router.post("/fornecedor/itens/{item_id}/alterar-foto")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def alterar_foto_item(request: Request, item_id: int, foto: UploadFile = File(...), usuario_logado: dict = {}):
    """Processa o upload de foto do item"""

    from util.image_processor import ImageProcessor
    from util.file_storage import FileStorageManager, TipoArquivo
    from config.constants import ImageConstants

    # Verificar se o item pertence ao fornecedor logado
    item = item_repo.obter_por_id(item_id)
    if not item or item.id_fornecedor != usuario_logado["id"]:
        logger.warning(
            "Tentativa de alterar foto de item não autorizado", item_id=item_id, fornecedor_id=usuario_logado["id"]
        )
        informar_erro(request, "Item não encontrado ou não autorizado")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    # Criar diretório se não existir
    FileStorageManager.criar_diretorio(TipoArquivo.ITEM)

    # Obter caminho físico para salvar
    caminho_arquivo = FileStorageManager.obter_caminho(TipoArquivo.ITEM, item_id, fisico=True)

    # Processar e salvar usando ImageProcessor
    sucesso, erro = await ImageProcessor.processar_e_salvar_imagem(
        foto, caminho_arquivo, tamanho=ImageConstants.Sizes.ITEM.value  # (600, 600)
    )

    if sucesso:
        logger.info("Foto do item alterada com sucesso", item_id=item_id, fornecedor_id=usuario_logado["id"])
        informar_sucesso(request, "Foto do item alterada com sucesso!")
    else:
        logger.warning("Erro ao alterar foto do item", item_id=item_id, erro=erro)
        informar_erro(request, f"Erro ao salvar foto: {erro}")

    return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/fornecedor/itens/{item_id}/remover-foto")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def remover_foto_item(request: Request, item_id: int, usuario_logado: dict = {}):
    """Remove a foto do item"""

    # Verificar se o item pertence ao fornecedor logado
    item = item_repo.obter_por_id(item_id)
    if not item or item.id_fornecedor != usuario_logado["id"]:
        logger.warning(
            "Tentativa de remover foto de item não autorizado", item_id=item_id, fornecedor_id=usuario_logado["id"]
        )
        informar_erro(request, "Item não encontrado ou não autorizado")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    if excluir_foto_item(item_id):
        logger.info("Foto do item removida com sucesso", item_id=item_id, fornecedor_id=usuario_logado["id"])
        informar_sucesso(request, "Foto do item removida com sucesso!")
    else:
        logger.warning("Nenhuma foto encontrada para remover", item_id=item_id)
        informar_aviso(request, "Nenhuma foto encontrada para remover")

    return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)
