from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from model.categoria_item_model import CategoriaItem
from model.item_model import TipoItem
from repo import usuario_repo, fornecedor_repo, item_repo, categoria_item_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ==================== DASHBOARD ====================

@router.get("/admin/dashboard")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def dashboard_admin(request: Request, usuario_logado: dict = None):
    """Dashboard principal do administrador"""
    try:
        # Estatísticas do sistema
        stats = {
            "total_usuarios": usuario_repo.contar_usuarios(),
            "total_fornecedores": fornecedor_repo.contar_fornecedores(),
            "fornecedores_nao_verificados": fornecedor_repo.contar_fornecedores_nao_verificados(),
            "total_itens": item_repo.contar_itens(),
            "estatisticas_itens": {
                "produtos": item_repo.contar_itens_por_tipo(TipoItem.PRODUTO),
                "servicos": item_repo.contar_itens_por_tipo(TipoItem.SERVICO),
                "espacos": item_repo.contar_itens_por_tipo(TipoItem.ESPACO)
            }
        }

        # Buscar fornecedores recentes
        fornecedores_recentes = fornecedor_repo.obter_fornecedores_por_pagina(1, 5)

        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats": stats,
            "fornecedores_recentes": fornecedores_recentes
        })
    except Exception as e:
        print(f"Erro no dashboard admin: {e}")
        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar estatísticas"
        })

# ==================== GESTÃO DE USUÁRIOS ====================

@router.get("/admin/usuarios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_usuarios(request: Request, usuario_logado: dict = None):
    """Lista todos os usuários do sistema"""
    try:
        usuarios = usuario_repo.obter_usuarios_por_pagina(1, 100)  # TODO: implementar paginação real
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "usuarios": usuarios
        })
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar usuários"
        })

@router.get("/admin/usuarios/{id_usuario}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def visualizar_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    """Visualiza detalhes de um usuário específico"""
    try:
        usuario = usuario_repo.obter_usuario_por_id(id_usuario)

        if not usuario:
            return templates.TemplateResponse("admin/usuarios.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Se for fornecedor, buscar dados adicionais
        fornecedor = None
        if usuario.perfil == TipoUsuario.FORNECEDOR:
            fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_usuario)

        return templates.TemplateResponse("admin/usuario_detalhes.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "usuario": usuario,
            "fornecedor": fornecedor
        })
    except Exception as e:
        print(f"Erro ao visualizar usuário: {e}")
        return templates.TemplateResponse("admin/usuarios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar usuário"
        })

# ==================== VERIFICAÇÃO DE FORNECEDORES ====================

@router.get("/admin/verificacao")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def verificacao_fornecedores(request: Request, usuario_logado: dict = None):
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
        print(f"Erro ao carregar verificação: {e}")
        return templates.TemplateResponse("admin/verificacao.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar fornecedores pendentes"
        })

@router.post("/admin/verificacao/{id_fornecedor}/aprovar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def aprovar_fornecedor(request: Request, id_fornecedor: int, usuario_logado: dict = None):
    """Aprova um fornecedor"""
    try:
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)
        if not fornecedor:
            return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

        fornecedor.verificado = True
        from datetime import datetime
        fornecedor.data_verificacao = datetime.now().isoformat()
        fornecedor_repo.atualizar_fornecedor(fornecedor)

        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao aprovar fornecedor: {e}")
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/verificacao/{id_fornecedor}/rejeitar")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def rejeitar_fornecedor(request: Request, id_fornecedor: int, observacoes: str = Form(""), usuario_logado: dict = None):
    """Rejeita um fornecedor"""
    try:
        fornecedor = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor)
        if not fornecedor:
            return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

        # Rejeitar fornecedor (remover verificação)
        sucesso = fornecedor_repo.rejeitar_fornecedor(id_fornecedor)

        if not sucesso:
            print(f"Falha ao rejeitar fornecedor {id_fornecedor}")

        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao rejeitar fornecedor: {e}")
        return RedirectResponse("/admin/verificacao", status_code=status.HTTP_303_SEE_OTHER)

# ==================== GESTÃO DE ITENS (VISUALIZAÇÃO) ====================

@router.get("/admin/itens")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_itens(request: Request, usuario_logado: dict = None):
    """Lista todos os itens do sistema"""
    try:
        itens = item_repo.obter_itens_por_pagina(1, 100)  # TODO: implementar paginação real

        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "itens": itens
        })
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return templates.TemplateResponse("admin/itens.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar itens"
        })

# ==================== RELATÓRIOS ====================

@router.get("/admin/relatorios")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def relatorios(request: Request, usuario_logado: dict = None):
    """Página de relatórios e estatísticas"""
    try:
        estatisticas = {
            "itens_por_tipo": item_repo.obter_estatisticas_itens(),
            "total_fornecedores": len(fornecedor_repo.obter_fornecedores_por_pagina(1, 1000)),
            "fornecedores_verificados": len([f for f in fornecedor_repo.obter_fornecedores_por_pagina(1, 1000) if f.verificado]),
            "total_prestadores": len(fornecedor_repo.obter_prestadores()),
            "total_vendedores": len(fornecedor_repo.obter_vendedores()),
            "total_locadores": len(fornecedor_repo.obter_locadores())
        }

        return templates.TemplateResponse("admin/relatorios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "estatisticas": estatisticas
        })
    except Exception as e:
        print(f"Erro ao gerar relatórios: {e}")
        return templates.TemplateResponse("admin/relatorios.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao gerar relatórios"
        })

# ==================== CATEGORIAS DE ITEM ====================

@router.get("/admin/categorias")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def listar_categorias(request: Request, usuario_logado: dict = None):
    """Lista todas as categorias de item"""
    try:
        categorias = categoria_item_repo.obter_todas_categorias()
        return templates.TemplateResponse("admin/categorias.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categorias": categorias,
            "tipos_item": [tipo for tipo in TipoItem]
        })
    except Exception as e:
        print(f"Erro ao listar categorias: {e}")
        return templates.TemplateResponse("admin/categorias.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro ao carregar categorias"
        })

@router.get("/admin/categoria/nova")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def nova_categoria(request: Request, usuario_logado: dict = None):
    """Formulário para criar nova categoria"""
    return templates.TemplateResponse("admin/categoria_form.html", {
        "request": request,
        "usuario_logado": usuario_logado,
        "tipos_item": [tipo for tipo in TipoItem],
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
    usuario_logado: dict = None
):
    """Cria uma nova categoria"""
    try:
        categoria = CategoriaItem(
            id=0,
            nome=nome,
            tipo_fornecimento=TipoItem(tipo_fornecimento),
            descricao=descricao if descricao else None,
            ativo=ativo
        )

        categoria_id = categoria_item_repo.inserir_categoria_item(categoria)
        if categoria_id:
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "criar",
                "erro": "Erro ao criar categoria"
            })
    except Exception as e:
        print(f"Erro ao criar categoria: {e}")
        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "tipos_item": [tipo for tipo in TipoItem],
            "acao": "criar",
            "erro": "Erro ao criar categoria"
        })

@router.get("/admin/categoria/editar/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def editar_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    """Formulário para editar categoria"""
    try:
        categoria = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
        if not categoria:
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categoria": categoria,
            "tipos_item": [tipo for tipo in TipoItem],
            "acao": "editar"
        })
    except Exception as e:
        print(f"Erro ao carregar categoria para edição: {e}")
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
    usuario_logado: dict = None
):
    """Atualiza uma categoria existente"""
    try:
        categoria = CategoriaItem(
            id=id_categoria,
            nome=nome,
            tipo_fornecimento=TipoItem(tipo_fornecimento),
            descricao=descricao if descricao else None,
            ativo=ativo
        )

        if categoria_item_repo.atualizar_categoria_item(categoria):
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
        else:
            categoria_atual = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
            return templates.TemplateResponse("admin/categoria_form.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "categoria": categoria_atual,
                "tipos_item": [tipo for tipo in TipoItem],
                "acao": "editar",
                "erro": "Erro ao atualizar categoria"
            })
    except Exception as e:
        print(f"Erro ao atualizar categoria: {e}")
        categoria_atual = categoria_item_repo.obter_categoria_item_por_id(id_categoria)
        return templates.TemplateResponse("admin/categoria_form.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "categoria": categoria_atual,
            "tipos_item": [tipo for tipo in TipoItem],
            "acao": "editar",
            "erro": "Erro ao atualizar categoria"
        })

@router.post("/admin/categoria/excluir/{id_categoria}")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def excluir_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    """Exclui uma categoria"""
    try:
        categoria_item_repo.excluir_categoria_item(id_categoria)
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(f"Erro ao excluir categoria: {e}")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

# ==================== CONFIGURAÇÕES ====================

@router.get("/admin/configuracoes")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def configuracoes(request: Request, usuario_logado: dict = None):
    """Página de configurações do sistema"""
    return templates.TemplateResponse("admin/configuracoes.html", {
        "request": request,
        "usuario_logado": usuario_logado
    })