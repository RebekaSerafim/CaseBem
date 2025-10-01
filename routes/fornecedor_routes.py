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
from core.repositories import fornecedor_repo, item_repo, orcamento_repo, demanda_repo, usuario_repo, categoria_repo, casal_repo
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso
from util.template_helpers import template_response_with_flash, configurar_filtros_jinja
from util.item_foto_util import excluir_foto_item
from decimal import Decimal

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

# Importar função centralizada de route_helpers
from util.route_helpers import get_active_page

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
    id_fornecedor = usuario_logado["id"]

    # Buscar dados do fornecedor
    fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)

    # Estatísticas dos itens do fornecedor
    total_itens = item_repo.contar_itens_por_fornecedor(id_fornecedor)
    meus_itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

    # Separar por tipo
    produtos = [item for item in meus_itens if item.tipo == TipoFornecimento.PRODUTO]
    servicos = [item for item in meus_itens if item.tipo == TipoFornecimento.SERVICO]
    espacos = [item for item in meus_itens if item.tipo == TipoFornecimento.ESPACO]

    # Buscar orçamentos do fornecedor
    try:
        orcamentos_fornecedor = orcamento_repo.obter_por_fornecedor_prestador(id_fornecedor)
        orcamentos_pendentes = [o for o in orcamentos_fornecedor if o.status == 'PENDENTE']
        orcamentos_aceitos = [o for o in orcamentos_fornecedor if o.status == 'ACEITO']
    except Exception as e:
        logger.warning("Erro ao buscar orçamentos do fornecedor", erro=e, fornecedor_id=id_fornecedor)
        orcamentos_fornecedor = []
        orcamentos_pendentes = []
        orcamentos_aceitos = []

    stats = {
        "total_itens": total_itens,
        "total_produtos": len(produtos),
        "total_servicos": len(servicos),
        "total_espacos": len(espacos),
        "status_verificacao": fornecedor.verificado if fornecedor else False,
        "total_orcamentos": len(orcamentos_fornecedor),
        "orcamentos_pendentes": len(orcamentos_pendentes),
        "orcamentos_aceitos": len(orcamentos_aceitos)
    }

    logger.info("Dashboard fornecedor carregado", fornecedor_id=id_fornecedor, total_itens=total_itens)

    return template_response_with_flash(templates, "fornecedor/dashboard.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "fornecedor": fornecedor,
        "stats": stats,
        "itens_recentes": meus_itens[:5]
    })

# ==================== GESTÃO DE ITENS ====================

@router.get("/fornecedor/itens")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/itens.html")
async def listar_itens(request: Request, usuario_logado: dict = {}):
    """Lista todos os itens do fornecedor"""
    id_fornecedor = usuario_logado["id"]
    meus_itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

    # Obter parâmetros de filtro
    search = request.query_params.get('search', '').strip()
    tipo_filter = request.query_params.get('tipo', '')
    status_filter = request.query_params.get('status', '')
    preco_max = request.query_params.get('preco_max', '')

    # Aplicar filtros
    itens_filtrados = meus_itens

    # Filtro por busca (nome ou descrição)
    if search:
        itens_filtrados = [
            item for item in itens_filtrados
            if search.lower() in item.nome.lower() or search.lower() in item.descricao.lower()
        ]

    # Filtro por tipo
    if tipo_filter:
        itens_filtrados = [
            item for item in itens_filtrados
            if item.tipo.value.lower() == tipo_filter.lower()
        ]

    # Filtro por status
    if status_filter:
        if status_filter == 'ativo':
            itens_filtrados = [item for item in itens_filtrados if item.ativo]
        elif status_filter == 'inativo':
            itens_filtrados = [item for item in itens_filtrados if not item.ativo]

    # Filtro por preço máximo
    if preco_max:
        try:
            preco_max_valor = float(preco_max)
            itens_filtrados = [item for item in itens_filtrados if item.preco <= preco_max_valor]
        except ValueError:
            logger.warning("Valor de preço máximo inválido", preco_max=preco_max)

    logger.info("Itens listados", fornecedor_id=id_fornecedor, total=len(itens_filtrados))

    return templates.TemplateResponse("fornecedor/itens.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "itens": itens_filtrados
    })

@router.get("/fornecedor/itens/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def novo_item_form(request: Request, usuario_logado: dict = {}):
    """Formulário para criar novo item"""
    categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
    return templates.TemplateResponse("fornecedor/item_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar",
        "tipos_item": [tipo.value for tipo in TipoFornecimento],
        "categorias": categorias
    })

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
    usuario_logado: dict = {}
):
    """Cria um novo item"""
    id_fornecedor = usuario_logado["id"]

    # Validar tipo
    try:
        tipo_enum = TipoFornecimento(tipo)
    except ValueError:
        logger.warning("Tipo de item inválido", tipo=tipo, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Tipo de item inválido",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

    # Validar categoria
    if not categoria:
        logger.warning("Categoria não fornecida", fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Categoria é obrigatória",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

    try:
        categoria_id = int(categoria)
    except ValueError:
        logger.warning("Categoria inválida", categoria=categoria, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Categoria inválida",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

    # Validar se categoria pertence ao tipo
    categoria_obj = categoria_repo.obter_por_id(categoria_id)
    if not categoria_obj or categoria_obj.tipo_fornecimento != tipo_enum:
        logger.warning("Categoria não pertence ao tipo", tipo=tipo, categoria_id=categoria_id, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": f"A categoria selecionada não pertence ao tipo {tipo_enum.value}",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

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
        id_categoria=categoria_id
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
            caminho_arquivo = FileStorageManager.obter_caminho(
                TipoArquivo.ITEM,
                item_id,
                fisico=True
            )

            # Processar e salvar usando ImageProcessor
            sucesso, erro = await ImageProcessor.processar_e_salvar_imagem(
                foto,
                caminho_arquivo,
                tamanho=ImageConstants.Sizes.ITEM.value  # (600, 600)
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
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao criar item",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

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
    return templates.TemplateResponse("fornecedor/item_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "editar",
        "item": item,
        "tipos_item": [tipo.value for tipo in TipoFornecimento],
        "categorias": categorias
    })

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
    usuario_logado: dict = {}
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
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Tipo de item inválido",
            "acao": "editar",
            "item": item_existente,
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

    # Validar categoria
    if not categoria:
        logger.warning("Categoria não fornecida ao atualizar", item_id=id_item)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Categoria é obrigatória",
            "acao": "editar",
            "item": item_existente,
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

    try:
        categoria_id = int(categoria)
    except ValueError:
        logger.warning("Categoria inválida ao atualizar", categoria=categoria, item_id=id_item)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Categoria inválida",
            "acao": "editar",
            "item": item_existente,
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

    # Validar se categoria pertence ao tipo
    categoria_obj_validacao = categoria_repo.obter_por_id(categoria_id)
    if not categoria_obj_validacao or categoria_obj_validacao.tipo_fornecimento != tipo_enum:
        logger.warning("Categoria não pertence ao tipo ao atualizar", tipo=tipo, categoria_id=categoria_id, item_id=id_item)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": f"A categoria selecionada não pertence ao tipo {tipo_enum.value}",
            "acao": "editar",
            "item": item_existente,
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

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
        id_categoria=categoria_id
    )

    sucesso = item_repo.atualizar(item_atualizado)

    if sucesso:
        logger.info("Item atualizado com sucesso", item_id=id_item, fornecedor_id=id_fornecedor, nome=nome)
        informar_sucesso(request, "Item atualizado com sucesso!")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    else:
        logger.error("Erro ao atualizar item no banco", item_id=id_item, fornecedor_id=id_fornecedor)
        categorias = [c for c in categoria_repo.buscar_categorias() if c.ativo]
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao atualizar item",
            "acao": "editar",
            "item": item_existente,
            "tipos_item": [tipo.value for tipo in TipoFornecimento],
            "categorias": categorias
        })

@router.post("/fornecedor/itens/{id_item}/excluir")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def excluir_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Exclui um item"""
    id_fornecedor = usuario_logado["id"]
    sucesso = item_repo.excluir(id_item, id_fornecedor)

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

            # Buscar dados do casal e noivo
            noivo = None
            if demanda:
                casal = casal_repo.obter_por_id(demanda.id_casal)
                if casal:
                    noivo = usuario_repo.obter_por_id(casal.id_noivo1)

            orcamento_data = {
                "orcamento": orcamento,
                "demanda": demanda,
                "noivo": noivo
            }
            orcamentos_enriched.append(orcamento_data)
        except Exception as e:
            logger.warning("Erro ao enriquecer orçamento", erro=e, orcamento_id=orcamento.id)
            # Adicionar mesmo com dados incompletos
            orcamentos_enriched.append({
                "orcamento": orcamento,
                "demanda": None,
                "noivo": None
            })

    logger.info("Orçamentos listados", fornecedor_id=id_fornecedor, total=len(orcamentos_enriched))
    return templates.TemplateResponse("fornecedor/orcamentos.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "orcamentos": orcamentos_enriched,
        "status_filter": status_filter
    })

@router.get("/fornecedor/demandas")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/demandas.html")
async def listar_demandas(request: Request, categoria: str = "", usuario_logado: dict = {}):
    """Lista demandas disponíveis para o fornecedor"""
    # Buscar todas as demandas ativas
    demandas = demanda_repo.obter_por_status(StatusDemanda.ATIVA.value)

    # Filtrar por categoria se especificado
    if categoria:
        try:
            categoria_id = int(categoria)
            demandas = [d for d in demandas if d.id_categoria == categoria_id]
        except ValueError:
            logger.warning("Categoria inválida no filtro", categoria=categoria)
            # Se categoria não for um número válido, ignorar o filtro
            pass

    # Enriquecer dados das demandas
    demandas_enriched = []
    for demanda in demandas:
        try:
            # Buscar dados do casal e noivo
            casal = casal_repo.obter_por_id(demanda.id_casal)
            noivo = None
            if casal:
                noivo = usuario_repo.obter_por_id(casal.id_noivo1)

            # Verificar se já existe orçamento deste fornecedor para esta demanda
            orcamentos_existentes = orcamento_repo.obter_por_demanda(demanda.id)
            ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

            demanda_data = {
                "demanda": demanda,
                "noivo": noivo,
                "ja_tem_orcamento": ja_tem_orcamento
            }
            demandas_enriched.append(demanda_data)
        except Exception as e:
            logger.warning("Erro ao enriquecer demanda", erro=e, demanda_id=demanda.id)
            demandas_enriched.append({
                "demanda": demanda,
                "noivo": None,
                "ja_tem_orcamento": False
            })

    logger.info("Demandas listadas", fornecedor_id=usuario_logado["id"], total=len(demandas_enriched))
    return templates.TemplateResponse("fornecedor/demandas.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "demandas": demandas_enriched,
        "categoria_filter": categoria
    })

@router.get("/fornecedor/demandas/{id_demanda}/propor")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/demandas")
async def form_propor_orcamento(request: Request, id_demanda: int, usuario_logado: dict = {}):
    """Formulário para propor orçamento para uma demanda"""
    # Buscar a demanda
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada ao propor orçamento", demanda_id=id_demanda)
        return RedirectResponse("/fornecedor/demandas?erro=demanda_nao_encontrada", status_code=status.HTTP_303_SEE_OTHER)

    # Buscar dados do casal e noivo
    casal = casal_repo.obter_por_id(demanda.id_casal)
    noivo = None
    if casal:
        noivo = usuario_repo.obter_por_id(casal.id_noivo1)

    # Verificar se já existe orçamento deste fornecedor para esta demanda
    orcamentos_existentes = orcamento_repo.obter_por_demanda(id_demanda)
    ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

    if ja_tem_orcamento:
        logger.warning("Fornecedor já tem orçamento para esta demanda", demanda_id=id_demanda, fornecedor_id=usuario_logado["id"])
        return RedirectResponse("/fornecedor/demandas?erro=ja_tem_orcamento", status_code=status.HTTP_303_SEE_OTHER)

    logger.info("Formulário de propor orçamento carregado", demanda_id=id_demanda, fornecedor_id=usuario_logado["id"])
    return templates.TemplateResponse("fornecedor/propor_orcamento.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "demanda": demanda,
        "noivo": noivo
    })

@router.post("/fornecedor/demandas/{id_demanda}/propor")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/demandas")
async def criar_orcamento(
    request: Request,
    id_demanda: int,
    valor_total: float = Form(...),
    observacoes: str = Form(""),
    data_validade: str = Form(None),
    usuario_logado: dict = {}
):
    """Cria um novo orçamento para uma demanda"""
    from datetime import datetime, timedelta
    from core.models.orcamento_model import Orcamento

    # Verificar se a demanda existe
    demanda = demanda_repo.obter_por_id(id_demanda)
    if not demanda:
        logger.warning("Demanda não encontrada ao criar orçamento", demanda_id=id_demanda)
        return RedirectResponse(f"/fornecedor/demandas/{id_demanda}/propor?erro=demanda_nao_encontrada", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se já existe orçamento deste fornecedor para esta demanda
    orcamentos_existentes = orcamento_repo.obter_por_demanda(id_demanda)
    ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

    if ja_tem_orcamento:
        logger.warning("Tentativa de criar orçamento duplicado", demanda_id=id_demanda, fornecedor_id=usuario_logado["id"])
        return RedirectResponse("/fornecedor/demandas?erro=ja_tem_orcamento", status_code=status.HTTP_303_SEE_OTHER)

    # Definir data de validade (padrão: 30 dias)
    if data_validade:
        try:
            data_hora_validade = datetime.strptime(data_validade, "%Y-%m-%d")
        except:
            logger.warning("Data de validade inválida, usando padrão de 30 dias", data_validade=data_validade)
            data_hora_validade = datetime.now() + timedelta(days=30)
    else:
        data_hora_validade = datetime.now() + timedelta(days=30)

    # Criar o orçamento
    novo_orcamento = Orcamento(
        id=0,
        id_demanda=id_demanda,
        id_fornecedor_prestador=usuario_logado["id"],
        data_hora_cadastro=datetime.now(),
        data_hora_validade=data_hora_validade,
        status="PENDENTE",
        observacoes=observacoes,
        valor_total=valor_total
    )

    # Inserir no banco
    id_orcamento = orcamento_repo.inserir(novo_orcamento)

    if id_orcamento:
        logger.info("Orçamento criado com sucesso", orcamento_id=id_orcamento, demanda_id=id_demanda, fornecedor_id=usuario_logado["id"])
        informar_sucesso(request, "Orçamento enviado com sucesso!")
        return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
    else:
        logger.error("Erro ao inserir orçamento no banco", demanda_id=id_demanda, fornecedor_id=usuario_logado["id"])
        informar_erro(request, "Erro ao criar orçamento!")
        return RedirectResponse(f"/fornecedor/demandas/{id_demanda}/propor", status_code=status.HTTP_303_SEE_OTHER)

# ==================== PERFIL ====================

@router.get("/fornecedor/perfil")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(template_erro="fornecedor/perfil.html")
async def perfil_fornecedor(request: Request, usuario_logado: dict = {}):
    """Página de perfil do fornecedor"""
    id_fornecedor = usuario_logado["id"]
    fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)

    logger.info("Perfil fornecedor carregado", fornecedor_id=id_fornecedor)
    return templates.TemplateResponse("fornecedor/perfil.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "fornecedor": fornecedor
    })

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
    usuario_logado: dict = {}
):
    """Atualiza perfil do fornecedor"""
    id_fornecedor = usuario_logado["id"]
    fornecedor = fornecedor_repo.obter_por_id(id_fornecedor)

    if not fornecedor:
        logger.error("Fornecedor não encontrado ao atualizar perfil", fornecedor_id=id_fornecedor)
        return templates.TemplateResponse("fornecedor/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Fornecedor não encontrado"
        })

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
        return templates.TemplateResponse("fornecedor/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor,
            "sucesso": "Perfil atualizado com sucesso!"
        })
    else:
        logger.error("Erro ao atualizar perfil no banco", fornecedor_id=id_fornecedor)
        return templates.TemplateResponse("fornecedor/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor,
            "erro": "Erro ao atualizar perfil"
        })

@router.post("/fornecedor/itens/{item_id}/alterar-foto")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
@tratar_erro_rota(redirect_erro="/fornecedor/itens")
async def alterar_foto_item(
    request: Request,
    item_id: int,
    foto: UploadFile = File(...),
    usuario_logado: dict = {}
):
    """Processa o upload de foto do item"""

    from util.image_processor import ImageProcessor
    from util.file_storage import FileStorageManager, TipoArquivo
    from config.constants import ImageConstants

    # Verificar se o item pertence ao fornecedor logado
    item = item_repo.obter_por_id(item_id)
    if not item or item.id_fornecedor != usuario_logado['id']:
        logger.warning("Tentativa de alterar foto de item não autorizado", item_id=item_id, fornecedor_id=usuario_logado['id'])
        informar_erro(request, "Item não encontrado ou não autorizado")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    # Criar diretório se não existir
    FileStorageManager.criar_diretorio(TipoArquivo.ITEM)

    # Obter caminho físico para salvar
    caminho_arquivo = FileStorageManager.obter_caminho(
        TipoArquivo.ITEM,
        item_id,
        fisico=True
    )

    # Processar e salvar usando ImageProcessor
    sucesso, erro = await ImageProcessor.processar_e_salvar_imagem(
        foto,
        caminho_arquivo,
        tamanho=ImageConstants.Sizes.ITEM.value  # (600, 600)
    )

    if sucesso:
        logger.info("Foto do item alterada com sucesso", item_id=item_id, fornecedor_id=usuario_logado['id'])
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
    if not item or item.id_fornecedor != usuario_logado['id']:
        logger.warning("Tentativa de remover foto de item não autorizado", item_id=item_id, fornecedor_id=usuario_logado['id'])
        informar_erro(request, "Item não encontrado ou não autorizado")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    if excluir_foto_item(item_id):
        logger.info("Foto do item removida com sucesso", item_id=item_id, fornecedor_id=usuario_logado['id'])
        informar_sucesso(request, "Foto do item removida com sucesso!")
    else:
        logger.warning("Nenhuma foto encontrada para remover", item_id=item_id)
        informar_aviso(request, "Nenhuma foto encontrada para remover")

    return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)