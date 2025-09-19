from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from repo import usuario_repo, fornecedor_repo, item_repo

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
            "total_usuarios": len(usuario_repo.obter_usuarios_por_pagina(1, 1000)),  # TODO: criar função count
            "total_fornecedores": len(fornecedor_repo.obter_fornecedores_por_pagina(1, 1000)),
            "fornecedores_nao_verificados": len([f for f in fornecedor_repo.obter_fornecedores_por_pagina(1, 1000) if not f.verificado]),
            "total_itens": len(item_repo.obter_itens_por_pagina(1, 1000)),
            "estatisticas_itens": item_repo.obter_estatisticas_itens()
        }

        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "stats": stats
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

        # TODO: Implementar lógica de rejeição
        # Por enquanto, apenas redireciona

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

# ==================== CONFIGURAÇÕES ====================

@router.get("/admin/configuracoes")
@requer_autenticacao([TipoUsuario.ADMIN.value])
async def configuracoes(request: Request, usuario_logado: dict = None):
    """Página de configurações do sistema"""
    return templates.TemplateResponse("admin/configuracoes.html", {
        "request": request,
        "usuario_logado": usuario_logado
    })