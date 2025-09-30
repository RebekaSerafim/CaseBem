"""
Serviço de favoritos - Lógica de negócio centralizada
"""

from typing import List
from util.exceptions import RegraDeNegocioError
from core.models.favorito_model import Favorito
from util.logger import logger


class FavoritoService:
    """Serviço para operações de negócio com favoritos"""

    def __init__(self):
        from core.repositories import favorito_repo, usuario_repo, item_repo

        self.repo = favorito_repo
        self.usuario_repo = usuario_repo
        self.item_repo = item_repo

    def adicionar_favorito(self, id_usuario: int, id_item: int) -> bool:
        """Adiciona um item aos favoritos"""
        # Validar que usuário e item existem
        self.usuario_repo.obter_por_id(id_usuario)
        self.item_repo.obter_por_id(id_item)

        # Verificar se já está nos favoritos
        try:
            favorito_existente = self.repo.obter_favorito(id_usuario, id_item)
            if favorito_existente:
                raise RegraDeNegocioError("Item já está nos favoritos")
        except:
            pass  # Não existe, pode adicionar

        favorito = Favorito(id_usuario=id_usuario, id_item=id_item)
        sucesso = self.repo.inserir(favorito)

        if sucesso:
            logger.info(f"Favorito adicionado: usuário={id_usuario}, item={id_item}")

        return sucesso

    def remover_favorito(self, id_usuario: int, id_item: int) -> bool:
        """Remove um item dos favoritos"""
        sucesso = self.repo.excluir(id_usuario, id_item)

        if sucesso:
            logger.info(f"Favorito removido: usuário={id_usuario}, item={id_item}")

        return sucesso

    def listar_favoritos(self, id_usuario: int) -> List[dict]:
        """Lista os favoritos de um usuário"""
        return self.repo.obter_favoritos_por_usuario(id_usuario)

    def verificar_favorito(self, id_usuario: int, id_item: int) -> bool:
        """Verifica se um item está nos favoritos"""
        try:
            favorito = self.repo.obter_favorito(id_usuario, id_item)
            return favorito is not None
        except:
            return False


favorito_service = FavoritoService()