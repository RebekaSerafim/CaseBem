import os

def obter_caminho_foto_item(item_id: int) -> str:
    """
    Retorna o caminho relativo da foto baseado no ID do item.

    Args:
        item_id: ID do item

    Returns:
        Caminho relativo da foto (ex: /static/img/itens/000001.jpg)
    """
    nome_arquivo = f"{item_id:06d}.jpg"
    return f"/static/img/itens/{nome_arquivo}"

def obter_caminho_foto_item_fisico(item_id: int) -> str:
    """
    Retorna o caminho físico absoluto para salvar o arquivo de foto do item.

    Args:
        item_id: ID do item

    Returns:
        Caminho físico absoluto do arquivo
    """
    nome_arquivo = f"{item_id:06d}.jpg"
    return f"static/img/itens/{nome_arquivo}"

def foto_item_existe(item_id: int) -> bool:
    """
    Verifica se a foto do item existe no sistema de arquivos.

    Args:
        item_id: ID do item

    Returns:
        True se a foto existe, False caso contrário
    """
    caminho_fisico = obter_caminho_foto_item_fisico(item_id)
    return os.path.exists(caminho_fisico)

def obter_foto_item_ou_padrao(item_id: int) -> str:
    """
    Retorna o caminho da foto do item ou imagem padrão se não existir.

    Args:
        item_id: ID do item

    Returns:
        Caminho da foto ou imagem padrão
    """
    if foto_item_existe(item_id):
        return obter_caminho_foto_item(item_id)
    return "/static/img/item-default.svg"

def excluir_foto_item(item_id: int) -> bool:
    """
    Exclui a foto do item do sistema de arquivos.

    Args:
        item_id: ID do item

    Returns:
        True se excluído com sucesso, False caso contrário
    """
    try:
        caminho_fisico = obter_caminho_foto_item_fisico(item_id)
        if os.path.exists(caminho_fisico):
            os.remove(caminho_fisico)
            return True
        return False
    except Exception as e:
        print(f"Erro ao excluir foto do item {item_id}: {e}")
        return False

def criar_diretorio_itens() -> bool:
    """
    Cria o diretório para armazenar fotos dos itens se não existir.

    Returns:
        True se criado com sucesso ou já existe, False caso contrário
    """
    try:
        diretorio = "static/img/itens"
        if not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório de itens: {e}")
        return False