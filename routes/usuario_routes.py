from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from repo import usuario_repo
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ==================== ALTERAÇÃO DE SENHA ====================

@router.get("/alterar-senha")
@requer_autenticacao([TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value])
async def get_alterar_senha(request: Request, usuario_logado: dict = None):
    """Página para alteração de senha (todos os perfis)"""
    return templates.TemplateResponse("alterar_senha.html", {
        "request": request,
        "usuario_logado": usuario_logado
    })

@router.post("/alterar-senha")
@requer_autenticacao([TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value])
async def post_alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: dict = None
):
    """Processa alteração de senha (todos os perfis)"""
    # Validar confirmação de senha
    if nova_senha != confirmar_senha:
        return templates.TemplateResponse("alterar_senha.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "A nova senha e confirmação não coincidem"
        })

    # Validar força da nova senha
    senha_valida, erro_senha = validar_forca_senha(nova_senha)
    if not senha_valida:
        return templates.TemplateResponse("alterar_senha.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": erro_senha
        })

    try:
        # Buscar usuário atual
        usuario = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
        if not usuario:
            return templates.TemplateResponse("alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Verificar senha atual
        if not verificar_senha(senha_atual, usuario.senha):
            return templates.TemplateResponse("alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Senha atual incorreta"
            })

        # Gerar hash da nova senha
        nova_senha_hash = criar_hash_senha(nova_senha)

        # Atualizar senha no banco
        sucesso = usuario_repo.atualizar_senha_usuario(usuario.id, nova_senha_hash)

        if sucesso:
            return templates.TemplateResponse("alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "sucesso": "Senha alterada com sucesso!"
            })
        else:
            return templates.TemplateResponse("alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao atualizar senha no banco de dados"
            })

    except Exception as e:
        print(f"Erro ao alterar senha: {e}")
        return templates.TemplateResponse("alterar_senha.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor"
        })