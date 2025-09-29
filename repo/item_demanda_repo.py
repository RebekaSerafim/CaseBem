from typing import Optional, List
from util.base_repo import BaseRepoChaveComposta
from sql import item_demanda_sql
from model.item_demanda_model import ItemDemanda

class ItemDemandaRepo(BaseRepoChaveComposta):
    """Repositório para operações com item_demanda (chave composta)"""

    def __init__(self):
        # ItemDemanda tem chave composta: (id_demanda, id_item)
        super().__init__('item_demanda', ItemDemanda, item_demanda_sql, ['id_demanda', 'id_item'])

    def _objeto_para_tupla_insert(self, item_demanda: ItemDemanda) -> tuple:
        """Prepara dados do item_demanda para inserção"""
        return (
            item_demanda.id_demanda,
            item_demanda.id_item,
            item_demanda.quantidade,
            item_demanda.observacoes,
            item_demanda.preco_maximo
        )

    def _objeto_para_tupla_update(self, item_demanda: ItemDemanda) -> tuple:
        """Prepara dados do item_demanda para atualização"""
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
            quantidade=linha.get("quantidade", 1),
            observacoes=linha.get("observacoes"),
            preco_maximo=linha.get("preco_maximo")
        )

    def obter_itens_por_demanda(self, id_demanda: int) -> List[dict]:
        """Obtém todos os itens de uma demanda com dados dos itens"""
        resultados = self.executar_query(item_demanda_sql.OBTER_ITENS_POR_DEMANDA, (id_demanda,))
        return [dict(resultado) for resultado in resultados]

    def excluir_itens_por_demanda(self, id_demanda: int) -> bool:
        """Exclui todos os itens de uma demanda"""
        return self.executar_comando(item_demanda_sql.EXCLUIR_ITENS_POR_DEMANDA, (id_demanda,))

# Instância global do repositório
item_demanda_repo = ItemDemandaRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_item_demanda() -> bool:
    return item_demanda_repo.criar_tabela()

def inserir_item_demanda(item_demanda: ItemDemanda) -> bool:
    return item_demanda_repo.inserir(item_demanda)

def atualizar_item_demanda(item_demanda: ItemDemanda) -> bool:
    return item_demanda_repo.atualizar(item_demanda)

def excluir_item_demanda(id_demanda: int, id_item: int) -> bool:
    return item_demanda_repo.excluir(id_demanda, id_item)

def obter_item_demanda(id_demanda: int, id_item: int) -> Optional[ItemDemanda]:
    return item_demanda_repo.obter_por_chave(id_demanda, id_item)

def obter_itens_por_demanda(id_demanda: int) -> List[dict]:
    return item_demanda_repo.obter_itens_por_demanda(id_demanda)

def excluir_itens_por_demanda(id_demanda: int) -> bool:
    return item_demanda_repo.excluir_itens_por_demanda(id_demanda)

def listar_item_demandas() -> List[ItemDemanda]:
    return item_demanda_repo.listar_todos()