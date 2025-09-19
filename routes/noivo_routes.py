from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from model.item_model import TipoItem
from repo import usuario_repo, item_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ==================== DASHBOARD ====================

@router.get("/noivo/dashboard")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def dashboard_noivo(request: Request, usuario_logado: dict = None):
    """Dashboard principal dos noivos"""
    try:
        id_noivo = usuario_logado["id"]

        # Buscar dados do noivo
        noivo = usuario_repo.obter_usuario_por_id(id_noivo)

        # TODO: Buscar dados do casal quando implementar casal_repo
        # casal = casal_repo.obter_casal_por_noivo(id_noivo)

        # Estatísticas para o noivo
        stats = {
            "total_produtos": len(item_repo.obter_produtos()),
            "total_servicos": len(item_repo.obter_servicos()),
            "total_espacos": len(item_repo.obter_espacos()),
            # TODO: Implementar quando tiver demanda_repo e orcamento_repo
            "minhas_demandas": 0,
            "orcamentos_recebidos": 0,
            "orcamentos_pendentes": 0
        }

        return templates.TemplateResponse("noivo/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "noivo": noivo,
            "stats": stats
        })
    except Exception as e:
        print(f"Erro no dashboard noivo: {e}")
        return templates.TemplateResponse("noivo/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar dashboard"
        })

# ==================== EXPLORAR ITENS ====================

@router.get("/noivo/produtos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_produtos(request: Request, usuario_logado: dict = None):
    """Lista produtos disponíveis"""
    try:
        produtos = item_repo.obter_produtos()

        return templates.TemplateResponse("noivo/produtos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "produtos": produtos
        })
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return templates.TemplateResponse("noivo/produtos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar produtos"
        })

@router.get("/noivo/servicos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_servicos(request: Request, usuario_logado: dict = None):
    """Lista serviços disponíveis"""
    try:
        servicos = item_repo.obter_servicos()

        return templates.TemplateResponse("noivo/servicos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "servicos": servicos
        })
    except Exception as e:
        print(f"Erro ao listar serviços: {e}")
        return templates.TemplateResponse("noivo/servicos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar serviços"
        })

@router.get("/noivo/espacos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_espacos(request: Request, usuario_logado: dict = None):
    """Lista espaços disponíveis"""
    try:
        espacos = item_repo.obter_espacos()

        return templates.TemplateResponse("noivo/espacos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "espacos": espacos
        })
    except Exception as e:
        print(f"Erro ao listar espaços: {e}")
        return templates.TemplateResponse("noivo/espacos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar espaços"
        })

@router.get("/noivo/buscar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def buscar_itens(request: Request, q: str = "", usuario_logado: dict = None):
    """Busca itens por termo"""
    try:
        resultados = []
        if q.strip():
            resultados = item_repo.buscar_itens(q.strip())

        return templates.TemplateResponse("noivo/buscar.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "resultados": resultados,
            "termo_busca": q
        })
    except Exception as e:
        print(f"Erro na busca: {e}")
        return templates.TemplateResponse("noivo/buscar.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro na busca",
            "termo_busca": q
        })

# ==================== DETALHES DE ITENS ====================

@router.get("/noivo/item/{id_item}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def visualizar_item(request: Request, id_item: int, usuario_logado: dict = None):
    """Visualiza detalhes de um item"""
    try:
        item = item_repo.obter_item_por_id(id_item)

        if not item or not item.ativo:
            return templates.TemplateResponse("noivo/item_nao_encontrado.html", {
                "request": request,
                "usuario_logado": usuario_logado
            })

        # TODO: Buscar dados do fornecedor quando implementar
        # fornecedor = fornecedor_repo.obter_fornecedor_por_id(item.id_fornecedor)

        return templates.TemplateResponse("noivo/item_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "item": item,
            "fornecedor": None  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao visualizar item: {e}")
        return templates.TemplateResponse("noivo/item_nao_encontrado.html", {
            "request": request,
            "usuario_logado": usuario_logado
        })

# ==================== DEMANDAS ====================

@router.get("/noivo/demandas")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_demandas(request: Request, usuario_logado: dict = None):
    """Lista demandas do noivo"""
    try:
        # TODO: Implementar quando tiver demanda_repo
        return templates.TemplateResponse("noivo/demandas.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "demandas": []  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao listar demandas: {e}")
        return templates.TemplateResponse("noivo/demandas.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar demandas"
        })

@router.get("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def nova_demanda_form(request: Request, usuario_logado: dict = None):
    """Formulário para criar nova demanda"""
    return templates.TemplateResponse("noivo/demanda_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar"
    })

@router.post("/noivo/demandas/nova")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def criar_demanda(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    orcamento_maximo: float = Form(0),
    data_evento: str = Form(""),
    usuario_logado: dict = None
):
    """Cria uma nova demanda"""
    try:
        # TODO: Implementar quando tiver demanda_repo
        # Por enquanto, apenas redireciona

        return RedirectResponse("/noivo/demandas", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao criar demanda: {e}")
        return templates.TemplateResponse("noivo/demanda_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao criar demanda",
            "acao": "criar"
        })

# ==================== ORÇAMENTOS ====================

@router.get("/noivo/orcamentos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_orcamentos(request: Request, usuario_logado: dict = None):
    """Lista orçamentos recebidos"""
    try:
        # TODO: Implementar quando tiver orcamento_repo
        return templates.TemplateResponse("noivo/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamentos": []  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao listar orçamentos: {e}")
        return templates.TemplateResponse("noivo/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar orçamentos"
        })

@router.get("/noivo/orcamentos/{id_orcamento}")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def visualizar_orcamento(request: Request, id_orcamento: int, usuario_logado: dict = None):
    """Visualiza detalhes de um orçamento"""
    try:
        # TODO: Implementar quando tiver orcamento_repo
        return templates.TemplateResponse("noivo/orcamento_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamento": None  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao visualizar orçamento: {e}")
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/noivo/orcamentos/{id_orcamento}/aceitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def aceitar_orcamento(request: Request, id_orcamento: int, usuario_logado: dict = None):
    """Aceita um orçamento"""
    try:
        # TODO: Implementar quando tiver orcamento_repo
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao aceitar orçamento: {e}")
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/noivo/orcamentos/{id_orcamento}/rejeitar")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def rejeitar_orcamento(request: Request, id_orcamento: int, usuario_logado: dict = None):
    """Rejeita um orçamento"""
    try:
        # TODO: Implementar quando tiver orcamento_repo
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao rejeitar orçamento: {e}")
        return RedirectResponse("/noivo/orcamentos", status_code=status.HTTP_303_SEE_OTHER)

# ==================== PERFIL E CASAL ====================

@router.get("/noivo/perfil")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def perfil_noivo(request: Request, usuario_logado: dict = None):
    """Página de perfil do noivo"""
    try:
        id_noivo = usuario_logado["id"]
        noivo = usuario_repo.obter_usuario_por_id(id_noivo)

        # TODO: Buscar dados do casal quando implementar
        # casal = casal_repo.obter_casal_por_noivo(id_noivo)

        return templates.TemplateResponse("noivo/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "noivo": noivo,
            "casal": None  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao carregar perfil: {e}")
        return templates.TemplateResponse("noivo/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar perfil"
        })

@router.post("/noivo/perfil")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def atualizar_perfil_noivo(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf: str = Form(""),
    data_nascimento: str = Form(""),
    usuario_logado: dict = None
):
    """Atualiza perfil do noivo"""
    try:
        id_noivo = usuario_logado["id"]
        noivo = usuario_repo.obter_usuario_por_id(id_noivo)

        if not noivo:
            return templates.TemplateResponse("noivo/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Atualizar dados
        noivo.nome = nome
        noivo.email = email
        noivo.telefone = telefone
        noivo.cpf = cpf if cpf else None
        noivo.data_nascimento = data_nascimento if data_nascimento else None

        sucesso = usuario_repo.atualizar_usuario(noivo)

        if sucesso:
            return templates.TemplateResponse("noivo/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "noivo": noivo,
                "sucesso": "Perfil atualizado com sucesso!"
            })
        else:
            return templates.TemplateResponse("noivo/perfil.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "noivo": noivo,
                "erro": "Erro ao atualizar perfil"
            })

    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return templates.TemplateResponse("noivo/perfil.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor"
        })

# ==================== FAVORITOS ====================

@router.get("/noivo/favoritos")
@requer_autenticacao([TipoUsuario.NOIVO.value])
async def listar_favoritos(request: Request, usuario_logado: dict = None):
    """Lista itens favoritos do noivo"""
    try:
        # TODO: Implementar sistema de favoritos
        return templates.TemplateResponse("noivo/favoritos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "favoritos": []  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao listar favoritos: {e}")
        return templates.TemplateResponse("noivo/favoritos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar favoritos"
        })