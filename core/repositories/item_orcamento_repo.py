from typing import Optional, List
from core.repositories.base_repo import BaseRepoChaveComposta
from infrastructure.logging import logger
from core.sql import item_orcamento_sql
from core.models.item_orcamento_model import ItemOrcamento


class ItemOrcamentoRepo(BaseRepoChaveComposta):
    """Repositório para operações com item_orcamento (tabela de relacionamento Orçamento-Item)"""

    def __init__(self):
        super().__init__(
            nome_tabela="item_orcamento",
            model_class=ItemOrcamento,
            sql_module=item_orcamento_sql,
            campos_chave=["id_orcamento", "id_item"],
        )

    def _objeto_para_tupla_insert(self, item_orcamento: ItemOrcamento) -> tuple:
        """Converte objeto ItemOrcamento em tupla para INSERT"""
        return (
            item_orcamento.id_orcamento,
            item_orcamento.id_item,
            item_orcamento.quantidade,
            item_orcamento.preco_unitario,
            item_orcamento.observacoes,
            item_orcamento.desconto,
        )

    def _objeto_para_tupla_update(self, item_orcamento: ItemOrcamento) -> tuple:
        """Converte objeto ItemOrcamento em tupla para UPDATE"""
        return (
            item_orcamento.quantidade,
            item_orcamento.preco_unitario,
            item_orcamento.observacoes,
            item_orcamento.desconto,
            item_orcamento.id_orcamento,
            item_orcamento.id_item,
        )

    def _linha_para_objeto(self, linha: dict) -> ItemOrcamento:
        """Converte linha do banco em objeto ItemOrcamento"""
        return ItemOrcamento(
            id_orcamento=linha["id_orcamento"],
            id_item=linha["id_item"],
            quantidade=linha["quantidade"],
            preco_unitario=linha["preco_unitario"],
            observacoes=linha["observacoes"],
            desconto=linha["desconto"],
        )

    def obter(self, id_orcamento: int, id_item: int) -> ItemOrcamento:
        """Obtém um item específico de um orçamento"""
        return self.obter_por_chave(id_orcamento, id_item)  # type: ignore[no-any-return]

    def obter_por_orcamento(self, id_orcamento: int) -> List[dict]:
        """Obtém todos os itens de um orçamento"""
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,)
        )
        return [dict(resultado) for resultado in resultados]

    def obter_total_orcamento(self, id_orcamento: int) -> float:
        """Calcula o total de um orçamento"""
        resultados = self.executar_consulta(
            item_orcamento_sql.OBTER_TOTAL_ORCAMENTO, (id_orcamento,)
        )
        if resultados and resultados[0]["total"]:
            return resultados[0]["total"]  # type: ignore[no-any-return]
        return 0.0

    def excluir_por_orcamento(self, id_orcamento: int) -> bool:
        """Exclui todos os itens de um orçamento"""
        return self.executar_comando(  # type: ignore[no-any-return]
            item_orcamento_sql.EXCLUIR_ITENS_POR_ORCAMENTO, (id_orcamento,)
        )


# Instância singleton do repositório
item_orcamento_repo = ItemOrcamentoRepo()
