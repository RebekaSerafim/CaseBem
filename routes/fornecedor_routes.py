from fastapi import APIRouter, Request, Form, status, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from model.demanda_model import StatusDemanda
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from model.item_model import Item, TipoItem
from repo import fornecedor_repo, item_repo, orcamento_repo, demanda_repo, usuario_repo, categoria_repo, casal_repo
from util.flash_messages import informar_sucesso, informar_erro, informar_aviso
from util.template_helpers import template_response_with_flash, configurar_filtros_jinja
from util.item_foto_util import (
    criar_diretorio_itens, obter_caminho_foto_item_fisico,
    excluir_foto_item, foto_item_existe
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

def get_fornecedor_active_page(request: Request) -> str:
    """Determina qual página está ativa na área fornecedor"""
    url_path = str(request.url.path)

    if url_path == "/fornecedor/dashboard":
        return "dashboard"
    elif url_path == "/fornecedor/perfil":
        return "perfil"
    elif url_path.startswith("/fornecedor/itens"):
        return "itens"
    elif url_path.startswith("/fornecedor/demandas"):
        return "demandas"
    elif url_path.startswith("/fornecedor/orcamentos"):
        return "orcamentos"
    else:
        return ""

# ==================== DASHBOARD ====================

@router.get("/fornecedor")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def root_fornecedor(request: Request, usuario_logado: dict = {}):
    return RedirectResponse("/fornecedor/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/fornecedor/dashboard")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def dashboard_fornecedor(request: Request, usuario_logado: dict = {}):
    """Dashboard principal do fornecedor"""
    try:
        id_fornecedor = usuario_logado["id"]

        # Buscar dados do fornecedor
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)

        # Estatísticas dos itens do fornecedor
        total_itens = item_repo.contar_itens_por_fornecedor(id_fornecedor)
        meus_itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

        # Separar por tipo
        produtos = [item for item in meus_itens if item.tipo == TipoItem.PRODUTO]
        servicos = [item for item in meus_itens if item.tipo == TipoItem.SERVICO]
        espacos = [item for item in meus_itens if item.tipo == TipoItem.ESPACO]

        # Buscar orçamentos do fornecedor
        try:
            orcamentos_fornecedor = orcamento_repo.obter_orcamentos_por_fornecedor_prestador(id_fornecedor)
            orcamentos_pendentes = [o for o in orcamentos_fornecedor if o.status == 'PENDENTE']
            orcamentos_aceitos = [o for o in orcamentos_fornecedor if o.status == 'ACEITO']
        except:
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

        return template_response_with_flash(templates, "fornecedor/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor,
            "stats": stats,
            "itens_recentes": meus_itens[:5]  # Últimos 5 itens
        })
    except Exception as e:
        print(f"Erro no dashboard fornecedor: {e}")
        return templates.TemplateResponse("fornecedor/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": None,
            "stats": {
                "total_itens": 0,
                "total_produtos": 0,
                "total_servicos": 0,
                "total_espacos": 0,
                "status_verificacao": False,
                "total_orcamentos": 0,
                "orcamentos_pendentes": 0,
                "orcamentos_aceitos": 0
            },
            "itens_recentes": [],
            "erro": "Erro ao carregar dashboard"
        })

# ==================== GESTÃO DE ITENS ====================

@router.get("/fornecedor/itens")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def listar_itens(request: Request, usuario_logado: dict = {}):
    """Lista todos os itens do fornecedor"""
    try:
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
                pass  # Ignorar se não for um número válido

        return templates.TemplateResponse("fornecedor/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "itens": itens_filtrados
        })
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return templates.TemplateResponse("fornecedor/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar itens",
            "itens": []
        })

@router.get("/fornecedor/itens/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def novo_item_form(request: Request, usuario_logado: dict = {}):
    """Formulário para criar novo item"""
    categorias = categoria_repo.obter_categorias_ativas()
    return templates.TemplateResponse("fornecedor/item_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar",
        "tipos_item": [tipo.value for tipo in TipoItem],
        "categorias": categorias
    })

@router.post("/fornecedor/itens/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
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
    try:
        id_fornecedor = usuario_logado["id"]

        # Validar tipo
        try:
            tipo_enum = TipoItem(tipo)
        except ValueError:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Tipo de item inválido",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        # Validar categoria
        if not categoria:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria é obrigatória",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        try:
            categoria_id = int(categoria)
        except ValueError:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria inválida",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        # Validar se categoria pertence ao tipo
        if not item_repo.validar_categoria_para_tipo(tipo_enum, categoria_id):
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": f"A categoria selecionada não pertence ao tipo {tipo_enum.value}",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        # Criar item
        novo_item = Item(
            id=0,
            id_fornecedor=id_fornecedor,
            tipo=tipo_enum,
            nome=nome,
            descricao=descricao,
            preco=preco,
            observacoes=observacoes if observacoes else None,
            ativo=True,
            data_cadastro=None,
            id_categoria=categoria_id
        )

        item_id = item_repo.inserir_item(novo_item)

        if item_id:
            # Processar foto se fornecida
            if foto and foto.filename:
                try:
                    # Validar tipo de arquivo
                    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
                    if foto.content_type in tipos_permitidos:
                        # Validar tamanho do arquivo (máximo 5MB)
                        conteudo_foto = await foto.read()
                        if len(conteudo_foto) <= 5 * 1024 * 1024:  # 5MB
                            # Criar diretório se não existir
                            criar_diretorio_itens()

                            # Obter caminho físico baseado no ID do item
                            caminho_arquivo = obter_caminho_foto_item_fisico(item_id)

                            # Processar imagem com Pillow
                            from io import BytesIO
                            imagem_bytes = BytesIO(conteudo_foto)
                            imagem = Image.open(imagem_bytes)

                            # Converter para RGB se necessário
                            if imagem.mode in ("RGBA", "P"):
                                imagem = imagem.convert("RGB")

                            # Redimensionar para 600x600 mantendo proporção
                            imagem.thumbnail((600, 600), Image.Resampling.LANCZOS)

                            # Criar uma imagem quadrada com fundo branco
                            imagem_quadrada = Image.new("RGB", (600, 600), (255, 255, 255))

                            # Centralizar a imagem redimensionada
                            x = (600 - imagem.width) // 2
                            y = (600 - imagem.height) // 2
                            imagem_quadrada.paste(imagem, (x, y))

                            # Salvar como JPG com qualidade 85%
                            imagem_quadrada.save(caminho_arquivo, "JPEG", quality=85, optimize=True)

                            informar_sucesso(request, "Item criado com sucesso e foto adicionada!")
                        else:
                            informar_sucesso(request, "Item criado com sucesso! Foto não salva - arquivo muito grande (máx. 5MB)")
                    else:
                        informar_sucesso(request, "Item criado com sucesso! Foto não salva - tipo de arquivo inválido")
                except Exception as e:
                    print(f"Erro ao processar foto do item {item_id}: {e}")
                    informar_sucesso(request, "Item criado com sucesso! Erro ao salvar foto")
            else:
                informar_sucesso(request, "Item criado com sucesso!")

            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
        else:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao criar item",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

    except Exception as e:
        print(f"Erro ao criar item: {e}")
        categorias = categoria_repo.obter_categorias_ativas()
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoItem],
            "categorias": categorias
        })

@router.get("/fornecedor/itens/{id_item}/editar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def editar_item_form(request: Request, id_item: int, usuario_logado: dict = {}):
    """Formulário para editar item"""
    try:
        id_fornecedor = usuario_logado["id"]
        item = item_repo.obter_item_por_id(id_item)

        if not item or item.id_fornecedor != id_fornecedor:
            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

        categorias = categoria_repo.obter_categorias_ativas()
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "editar",
            "item": item,
            "tipos_item": [tipo.value for tipo in TipoItem],
            "categorias": categorias
        })
    except Exception as e:
        print(f"Erro ao carregar formulário de edição: {e}")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/editar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
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
    try:
        id_fornecedor = usuario_logado["id"]

        # Verificar se o item pertence ao fornecedor
        item_existente = item_repo.obter_item_por_id(id_item)
        if not item_existente or item_existente.id_fornecedor != id_fornecedor:
            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

        # Validar tipo
        try:
            tipo_enum = TipoItem(tipo)
        except ValueError:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Tipo de item inválido",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        # Validar categoria
        if not categoria:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria é obrigatória",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        try:
            categoria_id = int(categoria)
        except ValueError:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Categoria inválida",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        # Validar se categoria pertence ao tipo
        if not item_repo.validar_categoria_para_tipo(tipo_enum, categoria_id):
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": f"A categoria selecionada não pertence ao tipo {tipo_enum.value}",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

        # Atualizar item
        item_atualizado = Item(
            id=id_item,
            id_fornecedor=id_fornecedor,
            tipo=tipo_enum,
            nome=nome,
            descricao=descricao,
            preco=preco,
            observacoes=observacoes if observacoes else None,
            ativo=ativo,
            data_cadastro=item_existente.data_cadastro,
            id_categoria=categoria_id
        )

        sucesso = item_repo.atualizar_item(item_atualizado)

        if sucesso:
            informar_sucesso(request, "Item atualizado com sucesso!")
            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
        else:
            categorias = categoria_repo.obter_categorias_ativas()
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao atualizar item",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem],
                "categorias": categorias
            })

    except Exception as e:
        print(f"Erro ao atualizar item: {e}")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/excluir")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def excluir_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Exclui um item"""
    try:
        id_fornecedor = usuario_logado["id"]
        sucesso = item_repo.excluir_item(id_item, id_fornecedor)

        if sucesso:
            informar_sucesso(request, "Item excluído com sucesso!")
        else:
            informar_erro(request, "Erro ao excluir item!")

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao excluir item: {e}")
        informar_erro(request, "Erro ao excluir item!")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/ativar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def ativar_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Ativa um item"""
    try:
        id_fornecedor = usuario_logado["id"]
        sucesso = item_repo.ativar_item(id_item, id_fornecedor)

        if sucesso:
            informar_sucesso(request, "Item ativado com sucesso!")
        else:
            informar_erro(request, "Erro ao ativar item!")

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao ativar item: {e}")
        informar_erro(request, "Erro ao ativar item!")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/desativar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def desativar_item(request: Request, id_item: int, usuario_logado: dict = {}):
    """Desativa um item"""
    try:
        id_fornecedor = usuario_logado["id"]
        sucesso = item_repo.desativar_item(id_item, id_fornecedor)

        if sucesso:
            informar_sucesso(request, "Item desativado com sucesso!")
        else:
            informar_erro(request, "Erro ao desativar item!")

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao desativar item: {e}")
        informar_erro(request, "Erro ao desativar item!")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

# ==================== ORÇAMENTOS ====================

@router.get("/fornecedor/orcamentos")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def listar_orcamentos(request: Request, status_filter: str = "", usuario_logado: dict = {}):
    """Lista orçamentos do fornecedor"""
    try:
        id_fornecedor = usuario_logado["id"]

        # Buscar orçamentos do fornecedor
        orcamentos = orcamento_repo.obter_orcamentos_por_fornecedor_prestador(id_fornecedor)

        # Filtrar por status se especificado
        if status_filter:
            orcamentos = [o for o in orcamentos if o.status.upper() == status_filter.upper()]

        # Enriquecer dados dos orçamentos
        orcamentos_enriched = []
        for orcamento in orcamentos:
            try:
                # Buscar dados da demanda
                demanda = demanda_repo.obter_demanda_por_id(orcamento.id_demanda)

                # Buscar dados do casal e noivo
                noivo = None
                if demanda:
                    casal = casal_repo.obter_casal_por_id(demanda.id_casal)
                    if casal:
                        noivo = usuario_repo.obter_usuario_por_id(casal.id_noivo1)

                orcamento_data = {
                    "orcamento": orcamento,
                    "demanda": demanda,
                    "noivo": noivo
                }
                orcamentos_enriched.append(orcamento_data)
            except Exception as e:
                print(f"Erro ao enriquecer orçamento {orcamento.id}: {e}")
                # Adicionar mesmo com dados incompletos
                orcamentos_enriched.append({
                    "orcamento": orcamento,
                    "demanda": None,
                    "noivo": None
                })

        return templates.TemplateResponse("fornecedor/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamentos": orcamentos_enriched,
            "status_filter": status_filter
        })
    except Exception as e:
        print(f"Erro ao listar orçamentos: {e}")
        return templates.TemplateResponse("fornecedor/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar orçamentos",
            "orcamentos": []
        })

@router.get("/fornecedor/demandas")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def listar_demandas(request: Request, categoria: str = "", usuario_logado: dict = {}):
    """Lista demandas disponíveis para o fornecedor"""
    try:
        # Buscar todas as demandas ativas
        demandas = demanda_repo.obter_demandas_por_status(StatusDemanda.ATIVA.value)

        # Filtrar por categoria se especificado
        if categoria:
            try:
                categoria_id = int(categoria)
                demandas = [d for d in demandas if d.id_categoria == categoria_id]
            except ValueError:
                # Se categoria não for um número válido, ignorar o filtro
                pass

        # Enriquecer dados das demandas
        demandas_enriched = []
        for demanda in demandas:
            try:
                # Buscar dados do casal e noivo
                casal = casal_repo.obter_casal_por_id(demanda.id_casal)
                noivo = None
                if casal:
                    noivo = usuario_repo.obter_usuario_por_id(casal.id_noivo1)

                # Verificar se já existe orçamento deste fornecedor para esta demanda
                orcamentos_existentes = orcamento_repo.obter_orcamentos_por_demanda(demanda.id)
                ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

                demanda_data = {
                    "demanda": demanda,
                    "noivo": noivo,
                    "ja_tem_orcamento": ja_tem_orcamento
                }
                demandas_enriched.append(demanda_data)
            except Exception as e:
                print(f"Erro ao enriquecer demanda {demanda.id}: {e}")
                demandas_enriched.append({
                    "demanda": demanda,
                    "noivo": None,
                    "ja_tem_orcamento": False
                })

        return templates.TemplateResponse("fornecedor/demandas.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "demandas": demandas_enriched,
            "categoria_filter": categoria
        })
    except Exception as e:
        print(f"Erro ao listar demandas: {e}")
        return templates.TemplateResponse("fornecedor/demandas.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar demandas",
            "demandas": []
        })

@router.get("/fornecedor/demandas/{id_demanda}/propor")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def form_propor_orcamento(request: Request, id_demanda: int, usuario_logado: dict = {}):
    """Formulário para propor orçamento para uma demanda"""
    try:
        # Buscar a demanda
        demanda = demanda_repo.obter_demanda_por_id(id_demanda)
        if not demanda:
            return RedirectResponse("/fornecedor/demandas?erro=demanda_nao_encontrada", status_code=status.HTTP_303_SEE_OTHER)

        # Buscar dados do casal e noivo
        casal = casal_repo.obter_casal_por_id(demanda.id_casal)
        noivo = None
        if casal:
            noivo = usuario_repo.obter_usuario_por_id(casal.id_noivo1)

        # Verificar se já existe orçamento deste fornecedor para esta demanda
        orcamentos_existentes = orcamento_repo.obter_orcamentos_por_demanda(id_demanda)
        ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

        if ja_tem_orcamento:
            return RedirectResponse("/fornecedor/demandas?erro=ja_tem_orcamento", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("fornecedor/propor_orcamento.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "demanda": demanda,
            "noivo": noivo
        })
    except Exception as e:
        print(f"Erro ao carregar formulário de orçamento: {e}")
        return RedirectResponse("/fornecedor/demandas?erro=erro_interno", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/demandas/{id_demanda}/propor")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def criar_orcamento(
    request: Request,
    id_demanda: int,
    valor_total: float = Form(...),
    observacoes: str = Form(""),
    data_validade: str = Form(None),
    usuario_logado: dict = {}
):
    """Cria um novo orçamento para uma demanda"""
    try:
        from datetime import datetime, timedelta
        from model.orcamento_model import Orcamento

        # Verificar se a demanda existe
        demanda = demanda_repo.obter_demanda_por_id(id_demanda)
        if not demanda:
            return RedirectResponse(f"/fornecedor/demandas/{id_demanda}/propor?erro=demanda_nao_encontrada", status_code=status.HTTP_303_SEE_OTHER)

        # Verificar se já existe orçamento deste fornecedor para esta demanda
        orcamentos_existentes = orcamento_repo.obter_orcamentos_por_demanda(id_demanda)
        ja_tem_orcamento = any(o.id_fornecedor_prestador == usuario_logado["id"] for o in orcamentos_existentes)

        if ja_tem_orcamento:
            return RedirectResponse("/fornecedor/demandas?erro=ja_tem_orcamento", status_code=status.HTTP_303_SEE_OTHER)

        # Definir data de validade (padrão: 30 dias)
        if data_validade:
            try:
                data_hora_validade = datetime.strptime(data_validade, "%Y-%m-%d")
            except:
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
        id_orcamento = orcamento_repo.inserir_orcamento(novo_orcamento)

        if id_orcamento:
            informar_sucesso(request, "Orçamento enviado com sucesso!")
            return RedirectResponse("/fornecedor/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
        else:
            informar_erro(request, "Erro ao criar orçamento!")
            return RedirectResponse(f"/fornecedor/demandas/{id_demanda}/propor", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"Erro ao criar orçamento: {e}")
        informar_erro(request, "Erro interno ao criar orçamento!")
        return RedirectResponse(f"/fornecedor/demandas/{id_demanda}/propor", status_code=status.HTTP_303_SEE_OTHER)

# ==================== PERFIL ====================

@router.get("/fornecedor/perfil")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def perfil_fornecedor(request: Request, usuario_logado: dict = {}):
    """Página de perfil do fornecedor"""
    try:
        id_fornecedor = usuario_logado["id"]
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)

        return templates.TemplateResponse("fornecedor/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao carregar perfil: {e}")
        return templates.TemplateResponse("fornecedor/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar perfil"
        })

@router.post("/fornecedor/perfil")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
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
    try:
        id_fornecedor = usuario_logado["id"]
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)

        if not fornecedor:
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

        sucesso = fornecedor_repo.atualizar_fornecedor(fornecedor)

        if sucesso:
            return templates.TemplateResponse("fornecedor/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "fornecedor": fornecedor,
                "sucesso": "Perfil atualizado com sucesso!"
            })
        else:
            return templates.TemplateResponse("fornecedor/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "fornecedor": fornecedor,
                "erro": "Erro ao atualizar perfil"
            })

    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return templates.TemplateResponse("fornecedor/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor"
        })

@router.post("/fornecedor/itens/{item_id}/alterar-foto")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def alterar_foto_item(
    request: Request,
    item_id: int,
    foto: UploadFile = File(...),
    usuario_logado: dict = {}
):
    """Processa o upload de foto do item"""

    # Verificar se o item pertence ao fornecedor logado
    item = item_repo.obter_item_por_id(item_id)
    if not item or item.id_fornecedor != usuario_logado['id']:
        informar_erro(request, "Item não encontrado ou não autorizado")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if foto.content_type not in tipos_permitidos:
        informar_erro(request, "Tipo de arquivo inválido. Use JPG, PNG ou WEBP")
        return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)

    # Validar tamanho do arquivo (máximo 5MB)
    conteudo = await foto.read()
    if len(conteudo) > 5 * 1024 * 1024:  # 5MB
        informar_erro(request, "Arquivo muito grande. Máximo 5MB")
        return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)

    try:
        # Criar diretório se não existir
        criar_diretorio_itens()

        # Obter caminho físico baseado no ID do item
        caminho_arquivo = obter_caminho_foto_item_fisico(item_id)

        # Processar imagem com Pillow
        try:
            # Criar uma nova instância BytesIO com o conteúdo
            from io import BytesIO
            imagem_bytes = BytesIO(conteudo)

            # Abrir imagem
            imagem = Image.open(imagem_bytes)

            # Converter para RGB se necessário (para salvar como JPG)
            if imagem.mode in ("RGBA", "P"):
                imagem = imagem.convert("RGB")

            # Redimensionar para 600x600 mantendo proporção
            imagem.thumbnail((600, 600), Image.Resampling.LANCZOS)

            # Criar uma imagem quadrada com fundo branco
            imagem_quadrada = Image.new("RGB", (600, 600), (255, 255, 255))

            # Centralizar a imagem redimensionada
            x = (600 - imagem.width) // 2
            y = (600 - imagem.height) // 2
            imagem_quadrada.paste(imagem, (x, y))

            # Salvar como JPG com qualidade 85%
            imagem_quadrada.save(caminho_arquivo, "JPEG", quality=85, optimize=True)

        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            informar_erro(request, "Erro ao processar imagem")
            return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)

        informar_sucesso(request, "Foto do item alterada com sucesso!")
        return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"Erro ao salvar foto do item {item_id}: {e}")
        informar_erro(request, "Erro interno do servidor")
        return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{item_id}/remover-foto")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def remover_foto_item(request: Request, item_id: int, usuario_logado: dict = {}):
    """Remove a foto do item"""

    # Verificar se o item pertence ao fornecedor logado
    item = item_repo.obter_item_por_id(item_id)
    if not item or item.id_fornecedor != usuario_logado['id']:
        informar_erro(request, "Item não encontrado ou não autorizado")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

    try:
        if excluir_foto_item(item_id):
            informar_sucesso(request, "Foto do item removida com sucesso!")
        else:
            informar_aviso(request, "Nenhuma foto encontrada para remover")

        return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"Erro ao remover foto do item {item_id}: {e}")
        informar_erro(request, "Erro interno do servidor")
        return RedirectResponse(f"/fornecedor/itens/{item_id}/editar", status_code=status.HTTP_303_SEE_OTHER)