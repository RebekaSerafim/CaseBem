from typing import Optional, List
from util.base_repo import BaseRepoChaveComposta
from core.sql import item_demanda_sql
from core.models.item_demanda_model import ItemDemanda

class ItemDemandaRepo(BaseRepoChaveComposta):
    """Repositório para operações com item_demanda (tabela de relacionamento Demanda-Item)"""

    def __init__(self):
        super().__init__(
            nome_tabela='item_demanda',
            model_class=ItemDemanda,
            sql_module=item_demanda_sql,
            campos_chave=['id_demanda', 'id_item']
        )

    def _objeto_para_tupla_insert(self, item_demanda: ItemDemanda) -> tuple:
        """Converte objeto ItemDemanda em tupla para INSERT"""
        return (
            item_demanda.id_demanda,
            item_demanda.id_item,
            item_demanda.quantidade,
            item_demanda.observacoes,
            item_demanda.preco_maximo
        )

    def _objeto_para_tupla_update(self, item_demanda: ItemDemanda) -> tuple:
        """Converte objeto ItemDemanda em tupla para UPDATE"""
        return (
            item_demanda.quantidade,
            item_demanda.observacoes,
            item_demanda.preco_maximo,
            item_demanda.id_demanda,
            item_demanda.id_item
        )

    def _linha_para_objeto(self, linha: dict) -> ItemDemanda:
        """Converte linha do banco em objeto ItemDemanda"""
        return ItemDemanda(
            id_demanda=linha["id_demanda"],
            id_item=linha["id_item"],
            quantidade=linha["quantidade"],
            observacoes=linha["observacoes"],
            preco_maximo=linha["preco_maximo"]
        )

    def obter(self, id_demanda: int, id_item: int) -> ItemDemanda:
        """Obtém um item específico de uma demanda"""
        return self.obter_por_chave(id_demanda, id_item)

    def obter_por_demanda(self, id_demanda: int) -> List[dict]:
        """Obtém todos os itens de uma demanda"""
        try:
            resultados = self.executar_query(
                item_demanda_sql.OBTER_ITENS_POR_DEMANDA,
                (id_demanda,)
            )
            return [dict(resultado) for resultado in resultados]
        except Exception as e:
            print(f"Erro ao obter itens por demanda: {e}")
            return []

    def excluir_por_demanda(self, id_demanda: int) -> bool:
        """Exclui todos os itens de uma demanda"""
        try:
            return self.executar_comando(
                item_demanda_sql.EXCLUIR_ITENS_POR_DEMANDA,
                (id_demanda,)
            )
        except Exception as e:
            print(f"Erro ao excluir itens por demanda: {e}")
            return False

# Instância singleton do repositório
item_demanda_repo = ItemDemandaRepo()