from fastapi import APIRouter, Request, Form, status, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from model.usuario_model import TipoUsuario
from repo import usuario_repo
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha
from util.template_helpers import configurar_filtros_jinja
from util.avatar_util import (
    obter_caminho_avatar_fisico,
    criar_diretorio_usuarios,
    excluir_avatar,
    obter_avatar_ou_padrao
)
import os
import secrets
from PIL import Image

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)

# ==================== ALTERAÇÃO DE SENHA ====================

@router.get("/alterar-senha")
@requer_autenticacao([TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value])
async def get_alterar_senha(request: Request, usuario_logado: dict = None):
    """Página para alteração de senha (todos os perfis)"""
    return templates.TemplateResponse("usuario/alterar_senha.html", {
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
        return templates.TemplateResponse("usuario/alterar_senha.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "A nova senha e confirmação não coincidem"
        })

    # Validar força da nova senha
    senha_valida, erro_senha = validar_forca_senha(nova_senha)
    if not senha_valida:
        return templates.TemplateResponse("usuario/alterar_senha.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": erro_senha
        })

    try:
        # Buscar usuário atual
        usuario = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
        if not usuario:
            return templates.TemplateResponse("usuario/alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Usuário não encontrado"
            })

        # Verificar senha atual
        if not verificar_senha(senha_atual, usuario.senha):
            return templates.TemplateResponse("usuario/alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Senha atual incorreta"
            })

        # Gerar hash da nova senha
        nova_senha_hash = criar_hash_senha(nova_senha)

        # Atualizar senha no banco
        sucesso = usuario_repo.atualizar_senha_usuario(usuario.id, nova_senha_hash)

        if sucesso:
            return templates.TemplateResponse("usuario/alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "sucesso": "Senha alterada com sucesso!"
            })
        else:
            return templates.TemplateResponse("usuario/alterar_senha.html", {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao atualizar senha no banco de dados"
            })

    except Exception as e:
        print(f"Erro ao alterar senha: {e}")
        return templates.TemplateResponse("usuario/alterar_senha.html", {
            "request": request,
            "usuario_logado": usuario_logado,
            "erro": "Erro interno do servidor"
        })

# ==================== UPLOAD DE AVATAR ====================

@router.post("/perfil/alterar-foto")
@requer_autenticacao([TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value])
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    """Processa o upload de avatar do usuário"""

    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if foto.content_type not in tipos_permitidos:
        # Redirecionar de volta com erro baseado no perfil
        perfil = usuario_logado['perfil'].lower()
        return RedirectResponse(f"/{perfil}/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # Validar tamanho do arquivo (máximo 5MB)
    conteudo = await foto.read()
    if len(conteudo) > 5 * 1024 * 1024:  # 5MB
        perfil = usuario_logado['perfil'].lower()
        return RedirectResponse(f"/{perfil}/perfil?erro=arquivo_muito_grande", status.HTTP_303_SEE_OTHER)

    try:
        # Criar diretório se não existir
        criar_diretorio_usuarios()

        # Obter caminho físico baseado no ID do usuário
        caminho_arquivo = obter_caminho_avatar_fisico(usuario_logado['id'])

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

            # Redimensionar para 300x300 mantendo proporção
            imagem.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Criar uma imagem quadrada com fundo branco
            imagem_quadrada = Image.new("RGB", (300, 300), (255, 255, 255))

            # Centralizar a imagem redimensionada
            x = (300 - imagem.width) // 2
            y = (300 - imagem.height) // 2
            imagem_quadrada.paste(imagem, (x, y))

            # Salvar como JPG
            imagem_quadrada.save(caminho_arquivo, "JPEG", quality=85)

        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            perfil = usuario_logado['perfil'].lower()
            return RedirectResponse(f"/{perfil}/perfil?erro=processamento_falhou", status.HTTP_303_SEE_OTHER)

        # Redirecionar com sucesso
        perfil = usuario_logado['perfil'].lower()
        return RedirectResponse(f"/{perfil}/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"Erro ao salvar avatar: {e}")
        perfil = usuario_logado['perfil'].lower()
        return RedirectResponse(f"/{perfil}/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

@router.post("/perfil/remover-foto")
@requer_autenticacao([TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value])
async def remover_foto(
    request: Request,
    usuario_logado: dict = None
):
    """Remove o avatar do usuário"""

    try:
        # Excluir avatar do sistema de arquivos
        excluir_avatar(usuario_logado['id'])

        # Redirecionar com sucesso
        perfil = usuario_logado['perfil'].lower()
        return RedirectResponse(f"/{perfil}/perfil?foto_removida=1", status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"Erro ao remover avatar: {e}")
        perfil = usuario_logado['perfil'].lower()
        return RedirectResponse(f"/{perfil}/perfil?erro=remocao_falhou", status.HTTP_303_SEE_OTHER)