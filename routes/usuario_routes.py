from fastapi import APIRouter, Request, Form, status, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from infrastructure.security import requer_autenticacao
from util.error_handlers import tratar_erro_rota
from infrastructure.logging import logger
from core.models.usuario_model import TipoUsuario
from core.repositories import usuario_repo
from infrastructure.security import (
    criar_hash_senha,
    verificar_senha,
    validar_forca_senha,
)
from util.template_helpers import configurar_filtros_jinja, TemplateRenderer
from util.avatar_util import excluir_avatar

router = APIRouter()
templates = Jinja2Templates(directory="templates")
configurar_filtros_jinja(templates)
renderer = TemplateRenderer(templates)

# ==================== ALTERAÇÃO DE SENHA ====================


@router.get("/alterar-senha")
@requer_autenticacao(
    [TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value]
)
async def get_alterar_senha(request: Request, _usuario_logado: dict = {}):
    """Página para alteração de senha (todos os perfis)"""
    return renderer.render(request, "usuario/alterar_senha.html")


@router.post("/alterar-senha")
@requer_autenticacao(
    [TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value]
)
@tratar_erro_rota(template_erro="usuario/alterar_senha.html")
async def post_alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: dict = {},
):
    """Processa alteração de senha (todos os perfis)"""
    # Validar confirmação de senha
    if nova_senha != confirmar_senha:
        logger.warning(
            f"Tentativa de alteração de senha com senhas não coincidentes - usuario_id: {usuario_logado['id']}"
        )
        return renderer.render(
            request,
            "usuario/alterar_senha.html",
            {"erro": "A nova senha e confirmação não coincidem"}
        )

    # Validar força da nova senha
    senha_valida, erro_senha = validar_forca_senha(nova_senha)
    if not senha_valida:
        logger.warning(
            f"Tentativa de alteração de senha com senha fraca - usuario_id: {usuario_logado['id']}, erro: {erro_senha}"
        )
        return renderer.render(
            request,
            "usuario/alterar_senha.html",
            {"erro": erro_senha}
        )

    # Buscar usuário atual
    usuario = usuario_repo.obter_por_id(usuario_logado["id"])
    if not usuario:
        logger.error(
            f"Usuário não encontrado ao alterar senha - usuario_id: {usuario_logado['id']}"
        )
        return renderer.render(
            request,
            "usuario/alterar_senha.html",
            {"erro": "Usuário não encontrado"}
        )

    # Verificar senha atual
    if not verificar_senha(senha_atual, usuario.senha):
        logger.warning(
            f"Senha atual incorreta ao alterar senha - usuario_id: {usuario_logado['id']}"
        )
        return renderer.render(
            request,
            "usuario/alterar_senha.html",
            {"erro": "Senha atual incorreta"}
        )

    # Gerar hash da nova senha
    nova_senha_hash = criar_hash_senha(nova_senha)

    # Atualizar senha no banco
    sucesso = usuario_repo.atualizar_senha_usuario(usuario.id, nova_senha_hash)

    if sucesso:
        logger.info(f"Senha alterada com sucesso - usuario_id: {usuario_logado['id']}")
        return renderer.render(
            request,
            "usuario/alterar_senha.html",
            {"sucesso": "Senha alterada com sucesso!"}
        )
    else:
        logger.error(
            f"Erro ao atualizar senha no banco de dados - usuario_id: {usuario_logado['id']}"
        )
        return renderer.render(
            request,
            "usuario/alterar_senha.html",
            {"erro": "Erro ao atualizar senha no banco de dados"}
        )


# ==================== UPLOAD DE AVATAR ====================


@router.post("/perfil/alterar-foto")
@requer_autenticacao(
    [TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value]
)
async def alterar_foto(
    _request: Request, foto: UploadFile = File(...), usuario_logado: dict = {}
):
    """Processa o upload de avatar do usuário"""
    from util.image_processor import ImageProcessor
    from util.file_storage import FileStorageManager, TipoArquivo
    from config.constants import ImageConstants

    perfil = usuario_logado["perfil"].lower()

    # Criar diretório se não existir
    FileStorageManager.criar_diretorio(TipoArquivo.USUARIO)

    # Obter caminho físico para salvar
    caminho_arquivo = FileStorageManager.obter_caminho(
        TipoArquivo.USUARIO,
        usuario_logado["id"],
        fisico=True
    )

    # Processar e salvar imagem usando ImageProcessor
    sucesso, erro = await ImageProcessor.processar_e_salvar_imagem(
        foto,
        caminho_arquivo,
        tamanho=ImageConstants.Sizes.AVATAR.value  # (300, 300)
    )

    if sucesso:
        logger.info(f"Avatar atualizado com sucesso - usuario_id: {usuario_logado['id']}")
        return RedirectResponse(
            f"/{perfil}/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER
        )
    else:
        logger.warning(
            f"Falha no upload de avatar - usuario_id: {usuario_logado['id']}, erro: {erro}"
        )
        return RedirectResponse(
            f"/{perfil}/perfil?erro={erro}", status.HTTP_303_SEE_OTHER
        )


@router.post("/perfil/remover-foto")
@requer_autenticacao(
    [TipoUsuario.ADMIN.value, TipoUsuario.FORNECEDOR.value, TipoUsuario.NOIVO.value]
)
async def remover_foto(_request: Request, usuario_logado: dict = {}):
    """Remove o avatar do usuário"""
    perfil = usuario_logado["perfil"].lower()

    try:
        # Excluir avatar do sistema de arquivos
        excluir_avatar(usuario_logado["id"])
        logger.info(f"Avatar removido com sucesso - usuario_id: {usuario_logado['id']}")

        # Redirecionar com sucesso
        return RedirectResponse(
            f"/{perfil}/perfil?foto_removida=1", status.HTTP_303_SEE_OTHER
        )

    except Exception as e:
        logger.error(
            f"Erro ao remover avatar - usuario_id: {usuario_logado['id']}, erro: {e}"
        )
        return RedirectResponse(
            f"/{perfil}/perfil?erro=remocao_falhou", status.HTTP_303_SEE_OTHER
        )
