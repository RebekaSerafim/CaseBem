from typing import Optional, List
from util.base_repo import BaseRepo
from util.logger import logger
from core.sql import favorito_sql
from core.models.favorito_model import Favorito

class FavoritoRepo(BaseRepo):
    """Repositório para operações com favoritos (tabela de relacionamento Noivo-Item)"""

    def __init__(self):
        super().__init__(
            nome_tabela='favorito',
            model_class=Favorito,
            sql_module=favorito_sql
        )

    def _objeto_para_tupla_insert(self, favorito: Favorito) -> tuple:
        """Converte objeto Favorito em tupla para INSERT"""
        return (
            favorito.id_noivo,
            favorito.id_item
        )

    def _objeto_para_tupla_update(self, favorito: Favorito) -> tuple:
        """Converte objeto Favorito em tupla para UPDATE"""
        return (
            favorito.id_noivo,
            favorito.id_item,
            favorito.id
        )

    def _linha_para_objeto(self, linha: dict) -> Favorito:
        """Converte linha do banco em objeto Favorito"""
        return Favorito(
            id=linha["id"],
            id_noivo=linha["id_noivo"],
            id_item=linha["id_item"],
            data_adicao=self._safe_get(linha, "data_adicao")
        )

    def adicionar(self, id_noivo: int, id_item: int) -> bool:
        """Adiciona um item aos favoritos do noivo"""
        favorito = Favorito(
            id=0,
            id_noivo=id_noivo,
            id_item=id_item,
            data_adicao=None
        )
        id_inserido = self.inserir(favorito)
        return id_inserido is not None and id_inserido > 0

    def remover(self, id_noivo: int, id_item: int) -> bool:
        """Remove um item dos favoritos do noivo"""
        return self.executar_comando(
            favorito_sql.EXCLUIR_FAVORITO,
            (id_noivo, id_item)
        )

    def obter_por_noivo(self, id_noivo: int) -> List[dict]:
        """Obtém todos os favoritos de um noivo com dados dos itens"""
        resultados = self.executar_query(
            favorito_sql.OBTER_FAVORITOS_POR_NOIVO,
            (id_noivo,)
        )
        return [dict(resultado) for resultado in resultados]

    def verificar(self, id_noivo: int, id_item: int) -> bool:
        """Verifica se um item está nos favoritos do noivo"""
        resultados = self.executar_query(
            favorito_sql.VERIFICAR_FAVORITO,
            (id_noivo, id_item)
        )
        return resultados[0]["count"] > 0 if resultados else False

    def contar_por_noivo(self, id_noivo: int) -> int:
        """Conta o total de favoritos de um noivo"""
        return self.contar_registros("id_noivo = ?", (id_noivo,))

# Instância singleton do repositório
favorito_repo = FavoritoRepo()