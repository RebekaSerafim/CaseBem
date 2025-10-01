"""
Serviço de favoritos - Lógica de negócio centralizada
"""

from typing import List
from util.exceptions import RegraDeNegocioError
from infrastructure.logging import logger


class FavoritoService:
    """Serviço para operações de negócio com favoritos"""

    def __init__(self):
        from core.repositories.favorito_repo import FavoritoRepo, favorito_repo
        from core.repositories.usuario_repo import UsuarioRepo, usuario_repo
        from core.repositories.item_repo import ItemRepo, item_repo

        self.repo: FavoritoRepo = favorito_repo
        self.usuario_repo: UsuarioRepo = usuario_repo
        self.item_repo: ItemRepo = item_repo

    def adicionar_favorito(self, id_usuario: int, id_item: int) -> bool:
        """Adiciona um item aos favoritos"""
        # Validar que usuário e item existem
        self.usuario_repo.obter_por_id(id_usuario)
        self.item_repo.obter_por_id(id_item)

        # Verificar se já está nos favoritos
        if self.repo.verificar(id_usuario, id_item):
            raise RegraDeNegocioError("Item já está nos favoritos")

        sucesso = self.repo.adicionar(id_usuario, id_item)

        if sucesso:
            logger.info(f"Favorito adicionado: usuário={id_usuario}, item={id_item}")

        return sucesso

    def remover_favorito(self, id_usuario: int, id_item: int) -> bool:
        """Remove um item dos favoritos"""
        sucesso = self.repo.remover(id_usuario, id_item)

        if sucesso:
            logger.info(f"Favorito removido: usuário={id_usuario}, item={id_item}")

        return sucesso

    def listar_favoritos(self, id_usuario: int) -> List[dict]:
        """Lista os favoritos de um usuário"""
        return self.repo.obter_por_noivo(id_usuario)

    def verificar_favorito(self, id_usuario: int, id_item: int) -> bool:
        """Verifica se um item está nos favoritos"""
        return self.repo.verificar(id_usuario, id_item)


favorito_service = FavoritoService()