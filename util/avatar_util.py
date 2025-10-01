import os

def obter_caminho_avatar(usuario_id: int) -> str:
    """
    Retorna o caminho relativo do avatar baseado no ID do usuário.

    Args:
        usuario_id: ID do usuário

    Returns:
        Caminho relativo do avatar (ex: /static/img/usuarios/000001.jpg)
    """
    nome_arquivo = f"{usuario_id:06d}.jpg"
    return f"/static/img/usuarios/{nome_arquivo}"

def obter_caminho_avatar_fisico(usuario_id: int) -> str:
    """
    Retorna o caminho físico absoluto para salvar o arquivo de avatar.

    Args:
        usuario_id: ID do usuário

    Returns:
        Caminho físico absoluto do arquivo
    """
    nome_arquivo = f"{usuario_id:06d}.jpg"
    return f"static/img/usuarios/{nome_arquivo}"

def avatar_existe(usuario_id: int) -> bool:
    """
    Verifica se o avatar do usuário existe no sistema de arquivos.

    Args:
        usuario_id: ID do usuário

    Returns:
        True se o avatar existe, False caso contrário
    """
    caminho_fisico = obter_caminho_avatar_fisico(usuario_id)
    return os.path.exists(caminho_fisico)

def obter_avatar_ou_padrao(usuario_id: int) -> str:
    """
    Retorna o caminho do avatar do usuário ou imagem padrão se não existir.

    Args:
        usuario_id: ID do usuário

    Returns:
        Caminho do avatar ou imagem padrão
    """
    if avatar_existe(usuario_id):
        return obter_caminho_avatar(usuario_id)
    return "/static/img/user-default.svg"

def excluir_avatar(usuario_id: int) -> bool:
    """
    Exclui o avatar do usuário do sistema de arquivos.

    Args:
        usuario_id: ID do usuário

    Returns:
        True se excluído com sucesso, False caso contrário
    """
    try:
        caminho_fisico = obter_caminho_avatar_fisico(usuario_id)
        if os.path.exists(caminho_fisico):
            os.remove(caminho_fisico)
            return True
        return False
    except Exception as e:
        print(f"Erro ao excluir avatar do usuário {usuario_id}: {e}")
        return False

def criar_diretorio_usuarios() -> bool:
    """
    Cria o diretório para armazenar avatares dos usuários se não existir.

    Returns:
        True se criado com sucesso ou já existe, False caso contrário
    """
    try:
        diretorio = "static/img/usuarios"
        if not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório de usuários: {e}")
        return False