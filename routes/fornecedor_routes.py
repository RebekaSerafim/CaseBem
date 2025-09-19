from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from model.item_model import Item, TipoItem
from repo import fornecedor_repo, item_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ==================== DASHBOARD ====================

@router.get("/fornecedor/dashboard")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def dashboard_fornecedor(request: Request, usuario_logado: dict = None):
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

        stats = {
            "total_itens": total_itens,
            "total_produtos": len(produtos),
            "total_servicos": len(servicos),
            "total_espacos": len(espacos),
            "status_verificacao": fornecedor.verificado if fornecedor else False
        }

        return templates.TemplateResponse("fornecedor/dashboard.html", {
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
            "erro": "Erro ao carregar dashboard"
        })

# ==================== GESTÃO DE ITENS ====================

@router.get("/fornecedor/itens")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def listar_itens(request: Request, usuario_logado: dict = None):
    """Lista todos os itens do fornecedor"""
    try:
        id_fornecedor = usuario_logado["id"]
        meus_itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

        return templates.TemplateResponse("fornecedor/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "itens": meus_itens
        })
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return templates.TemplateResponse("fornecedor/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar itens"
        })

@router.get("/fornecedor/itens/novo")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def novo_item_form(request: Request, usuario_logado: dict = None):
    """Formulário para criar novo item"""
    return templates.TemplateResponse("fornecedor/item_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "acao": "criar",
        "tipos_item": [tipo.value for tipo in TipoItem]
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
    usuario_logado: dict = None
):
    """Cria um novo item"""
    try:
        id_fornecedor = usuario_logado["id"]

        # Validar tipo
        try:
            tipo_enum = TipoItem(tipo)
        except ValueError:
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Tipo de item inválido",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem]
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
            data_cadastro=None
        )

        item_id = item_repo.inserir_item(novo_item)

        if item_id:
            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao criar item",
                "acao": "criar",
                "tipos_item": [tipo.value for tipo in TipoItem]
            })

    except Exception as e:
        print(f"Erro ao criar item: {e}")
        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor",
            "acao": "criar",
            "tipos_item": [tipo.value for tipo in TipoItem]
        })

@router.get("/fornecedor/itens/{id_item}/editar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def editar_item_form(request: Request, id_item: int, usuario_logado: dict = None):
    """Formulário para editar item"""
    try:
        id_fornecedor = usuario_logado["id"]
        item = item_repo.obter_item_por_id(id_item)

        if not item or item.id_fornecedor != id_fornecedor:
            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("fornecedor/item_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "acao": "editar",
            "item": item,
            "tipos_item": [tipo.value for tipo in TipoItem]
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
    ativo: bool = Form(True),
    usuario_logado: dict = None
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
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Tipo de item inválido",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem]
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
            data_cadastro=item_existente.data_cadastro
        )

        sucesso = item_repo.atualizar_item(item_atualizado)

        if sucesso:
            return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("fornecedor/item_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao atualizar item",
                "acao": "editar",
                "item": item_existente,
                "tipos_item": [tipo.value for tipo in TipoItem]
            })

    except Exception as e:
        print(f"Erro ao atualizar item: {e}")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/excluir")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def excluir_item(request: Request, id_item: int, usuario_logado: dict = None):
    """Exclui um item"""
    try:
        id_fornecedor = usuario_logado["id"]
        sucesso = item_repo.excluir_item(id_item, id_fornecedor)

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao excluir item: {e}")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/ativar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def ativar_item(request: Request, id_item: int, usuario_logado: dict = None):
    """Ativa um item"""
    try:
        id_fornecedor = usuario_logado["id"]
        item_repo.ativar_item(id_item, id_fornecedor)

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao ativar item: {e}")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/fornecedor/itens/{id_item}/desativar")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def desativar_item(request: Request, id_item: int, usuario_logado: dict = None):
    """Desativa um item"""
    try:
        id_fornecedor = usuario_logado["id"]
        item_repo.desativar_item(id_item, id_fornecedor)

        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao desativar item: {e}")
        return RedirectResponse("/fornecedor/itens", status_code=status.HTTP_303_SEE_OTHER)

# ==================== ORÇAMENTOS ====================

@router.get("/fornecedor/orcamentos")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def listar_orcamentos(request: Request, usuario_logado: dict = None):
    """Lista orçamentos do fornecedor"""
    try:
        # TODO: Implementar quando tiver o repositório de orçamentos
        return templates.TemplateResponse("fornecedor/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "orcamentos": []  # Placeholder
        })
    except Exception as e:
        print(f"Erro ao listar orçamentos: {e}")
        return templates.TemplateResponse("fornecedor/orcamentos.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar orçamentos"
        })

# ==================== PERFIL ====================

@router.get("/fornecedor/perfil")
@requer_autenticacao([TipoUsuario.FORNECEDOR.value])
async def perfil_fornecedor(request: Request, usuario_logado: dict = None):
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
    prestador: bool = Form(False),
    vendedor: bool = Form(False),
    locador: bool = Form(False),
    usuario_logado: dict = None
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

        # Atualizar dados
        fornecedor.nome = nome
        fornecedor.email = email
        fornecedor.telefone = telefone
        fornecedor.nome_empresa = nome_empresa
        fornecedor.cnpj = cnpj
        fornecedor.descricao = descricao
        fornecedor.prestador = prestador
        fornecedor.vendedor = vendedor
        fornecedor.locador = locador

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