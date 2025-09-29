from typing import Optional, List
from util.base_repo import BaseRepoChaveComposta
from sql import item_orcamento_sql
from model.item_orcamento_model import ItemOrcamento

class ItemOrcamentoRepo(BaseRepoChaveComposta):
    """Repositório para operações com item_orcamento (chave composta)"""

    def __init__(self):
        # ItemOrcamento tem chave composta: (id_orcamento, id_item)
        super().__init__('item_orcamento', ItemOrcamento, item_orcamento_sql, ['id_orcamento', 'id_item'])

    def _objeto_para_tupla_insert(self, item_orcamento: ItemOrcamento) -> tuple:
        """Prepara dados do item_orcamento para inserção"""
        return (
            item_orcamento.id_orcamento,
            item_orcamento.id_item,
            item_orcamento.quantidade,
            item_orcamento.preco_unitario,
            item_orcamento.observacoes,
            item_orcamento.desconto
        )

    def _objeto_para_tupla_update(self, item_orcamento: ItemOrcamento) -> tuple:
        """Prepara dados do item_orcamento para atualização"""
        return (
            item_orcamento.quantidade,
            item_orcamento.preco_unitario,
            item_orcamento.observacoes,
            item_orcamento.desconto,
            item_orcamento.id_orcamento,
            item_orcamento.id_item
        )

    def _linha_para_objeto(self, linha: dict) -> ItemOrcamento:
        """Converte linha do banco em objeto ItemOrcamento"""
        return ItemOrcamento(
            id_orcamento=linha["id_orcamento"],
            id_item=linha["id_item"],
            quantidade=linha.get("quantidade", 1),
            preco_unitario=linha.get("preco_unitario", 0.0),
            observacoes=linha.get("observacoes"),
            desconto=linha.get("desconto", 0.0)
        )

    def obter_itens_por_orcamento(self, id_orcamento: int) -> List[dict]:
        """Obtém todos os itens de um orçamento com dados dos itens"""
        resultados = self.executar_query(item_orcamento_sql.OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,))
        return [dict(resultado) for resultado in resultados]

    def obter_total_orcamento(self, id_orcamento: int) -> float:
        """Calcula o total de um orçamento"""
        resultados = self.executar_query(item_orcamento_sql.OBTER_TOTAL_ORCAMENTO, (id_orcamento,))
        if resultados:
            return resultados[0]["total"] or 0.0
        return 0.0

    def excluir_itens_por_orcamento(self, id_orcamento: int) -> bool:
        """Exclui todos os itens de um orçamento"""
        return self.executar_comando(item_orcamento_sql.EXCLUIR_ITENS_POR_ORCAMENTO, (id_orcamento,))

# Instância global do repositório
item_orcamento_repo = ItemOrcamentoRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_item_orcamento() -> bool:
    return item_orcamento_repo.criar_tabela()

def inserir_item_orcamento(item_orcamento: ItemOrcamento) -> bool:
    return item_orcamento_repo.inserir(item_orcamento)

def atualizar_item_orcamento(item_orcamento: ItemOrcamento) -> bool:
    return item_orcamento_repo.atualizar(item_orcamento)

def excluir_item_orcamento(id_orcamento: int, id_item: int) -> bool:
    return item_orcamento_repo.excluir(id_orcamento, id_item)

def obter_item_orcamento(id_orcamento: int, id_item: int) -> Optional[ItemOrcamento]:
    return item_orcamento_repo.obter_por_chave(id_orcamento, id_item)

def obter_itens_por_orcamento(id_orcamento: int) -> List[dict]:
    return item_orcamento_repo.obter_itens_por_orcamento(id_orcamento)

def obter_total_orcamento(id_orcamento: int) -> float:
    return item_orcamento_repo.obter_total_orcamento(id_orcamento)

def excluir_itens_por_orcamento(id_orcamento: int) -> bool:
    return item_orcamento_repo.excluir_itens_por_orcamento(id_orcamento)

def listar_item_orcamentos() -> List[ItemOrcamento]:
    return item_orcamento_repo.listar_todos()