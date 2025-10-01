"""
Gerenciador centralizado de armazenamento de arquivos.

Este módulo substitui avatar_util.py e item_foto_util.py,
consolidando a lógica duplicada de gerenciamento de arquivos.
"""

from enum import Enum
import os


class TipoArquivo(Enum):
    """Tipos de arquivo gerenciados pelo sistema"""
    USUARIO = "usuarios"
    ITEM = "itens"


class FileStorageManager:
    """Gerenciador centralizado de armazenamento de arquivos"""

    BASE_DIR = "static/img"
    BASE_URL = "/static/img"

    # Arquivos padrão quando não há imagem personalizada
    DEFAULTS = {
        TipoArquivo.USUARIO: "/static/img/user-default.svg",
        TipoArquivo.ITEM: "/static/img/item-default.svg"
    }

    @staticmethod
    def obter_caminho(
        tipo: TipoArquivo,
        id_recurso: int,
        fisico: bool = False
    ) -> str:
        """
        Obtém caminho do arquivo (web ou físico).

        Args:
            tipo: Tipo de arquivo (USUARIO ou ITEM)
            id_recurso: ID do recurso
            fisico: Se True, retorna caminho físico; se False, retorna URL web

        Returns:
            str: Caminho do arquivo

        Examples:
            >>> FileStorageManager.obter_caminho(TipoArquivo.USUARIO, 42, fisico=False)
            '/static/img/usuarios/000042.jpg'
            >>> FileStorageManager.obter_caminho(TipoArquivo.USUARIO, 42, fisico=True)
            'static/img/usuarios/000042.jpg'
        """
        nome_arquivo = f"{id_recurso:06d}.jpg"
        subdir = tipo.value

        if fisico:
            return f"{FileStorageManager.BASE_DIR}/{subdir}/{nome_arquivo}"
        return f"{FileStorageManager.BASE_URL}/{subdir}/{nome_arquivo}"

    @staticmethod
    def arquivo_existe(tipo: TipoArquivo, id_recurso: int) -> bool:
        """
        Verifica se arquivo existe no sistema.

        Args:
            tipo: Tipo de arquivo
            id_recurso: ID do recurso

        Returns:
            bool: True se arquivo existe, False caso contrário
        """
        caminho = FileStorageManager.obter_caminho(tipo, id_recurso, fisico=True)
        return os.path.exists(caminho)

    @staticmethod
    def obter_ou_padrao(tipo: TipoArquivo, id_recurso: int) -> str:
        """
        Retorna arquivo personalizado ou padrão.

        Args:
            tipo: Tipo de arquivo
            id_recurso: ID do recurso

        Returns:
            str: URL do arquivo personalizado ou padrão
        """
        if FileStorageManager.arquivo_existe(tipo, id_recurso):
            return FileStorageManager.obter_caminho(tipo, id_recurso, fisico=False)

        return FileStorageManager.DEFAULTS[tipo]

    @staticmethod
    def excluir(tipo: TipoArquivo, id_recurso: int) -> bool:
        """
        Exclui arquivo do sistema.

        Args:
            tipo: Tipo de arquivo
            id_recurso: ID do recurso

        Returns:
            bool: True se arquivo foi excluído, False se não existia ou erro
        """
        try:
            caminho = FileStorageManager.obter_caminho(tipo, id_recurso, fisico=True)
            if os.path.exists(caminho):
                os.remove(caminho)
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir arquivo {tipo.value} ID {id_recurso}: {e}")
            return False

    @staticmethod
    def criar_diretorio(tipo: TipoArquivo) -> bool:
        """
        Cria diretório para o tipo de arquivo se não existir.

        Args:
            tipo: Tipo de arquivo

        Returns:
            bool: True se criou ou já existia, False em caso de erro
        """
        try:
            diretorio = f"{FileStorageManager.BASE_DIR}/{tipo.value}"
            os.makedirs(diretorio, exist_ok=True)
            return True
        except Exception as e:
            print(f"Erro ao criar diretório {tipo.value}: {e}")
            return False

    @staticmethod
    def listar_arquivos(tipo: TipoArquivo) -> list:
        """
        Lista todos os arquivos de um tipo.

        Args:
            tipo: Tipo de arquivo

        Returns:
            list: Lista de IDs que possuem arquivo
        """
        try:
            diretorio = f"{FileStorageManager.BASE_DIR}/{tipo.value}"
            if not os.path.exists(diretorio):
                return []

            arquivos = os.listdir(diretorio)
            # Extrair IDs dos nomes de arquivo (000042.jpg -> 42)
            ids = []
            for arquivo in arquivos:
                if arquivo.endswith('.jpg'):
                    try:
                        id_recurso = int(arquivo.replace('.jpg', ''))
                        ids.append(id_recurso)
                    except ValueError:
                        continue

            return sorted(ids)
        except Exception as e:
            print(f"Erro ao listar arquivos {tipo.value}: {e}")
            return []


# Funções de compatibilidade para facilitar migração gradual

def obter_caminho_avatar(usuario_id: int) -> str:
    """DEPRECATED: Use FileStorageManager.obter_caminho(TipoArquivo.USUARIO, usuario_id)"""
    return FileStorageManager.obter_caminho(TipoArquivo.USUARIO, usuario_id, fisico=False)


def obter_caminho_avatar_fisico(usuario_id: int) -> str:
    """DEPRECATED: Use FileStorageManager.obter_caminho(TipoArquivo.USUARIO, usuario_id, fisico=True)"""
    return FileStorageManager.obter_caminho(TipoArquivo.USUARIO, usuario_id, fisico=True)


def avatar_existe(usuario_id: int) -> bool:
    """DEPRECATED: Use FileStorageManager.arquivo_existe(TipoArquivo.USUARIO, usuario_id)"""
    return FileStorageManager.arquivo_existe(TipoArquivo.USUARIO, usuario_id)


def obter_avatar_ou_padrao(usuario_id: int) -> str:
    """DEPRECATED: Use FileStorageManager.obter_ou_padrao(TipoArquivo.USUARIO, usuario_id)"""
    return FileStorageManager.obter_ou_padrao(TipoArquivo.USUARIO, usuario_id)


def obter_caminho_foto_item(item_id: int) -> str:
    """DEPRECATED: Use FileStorageManager.obter_caminho(TipoArquivo.ITEM, item_id)"""
    return FileStorageManager.obter_caminho(TipoArquivo.ITEM, item_id, fisico=False)


def obter_caminho_foto_item_fisico(item_id: int) -> str:
    """DEPRECATED: Use FileStorageManager.obter_caminho(TipoArquivo.ITEM, item_id, fisico=True)"""
    return FileStorageManager.obter_caminho(TipoArquivo.ITEM, item_id, fisico=True)


def foto_item_existe(item_id: int) -> bool:
    """DEPRECATED: Use FileStorageManager.arquivo_existe(TipoArquivo.ITEM, item_id)"""
    return FileStorageManager.arquivo_existe(TipoArquivo.ITEM, item_id)


def obter_foto_item_ou_padrao(item_id: int) -> str:
    """DEPRECATED: Use FileStorageManager.obter_ou_padrao(TipoArquivo.ITEM, item_id)"""
    return FileStorageManager.obter_ou_padrao(TipoArquivo.ITEM, item_id)
