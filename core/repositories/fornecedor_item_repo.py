from typing import Optional, List
from core.repositories.base_repo import BaseRepoChaveComposta
from util.logger import logger
from core.sql import fornecedor_item_sql
from core.models.fornecedor_item_model import FornecedorItem
from core.models.tipo_fornecimento_model import TipoFornecimento


class FornecedorItemRepo(BaseRepoChaveComposta):
    """Repositório para operações com fornecedor_item (tabela de relacionamento Fornecedor-Item)"""

    def __init__(self):
        super().__init__(
            nome_tabela="fornecedor_item",
            model_class=FornecedorItem,
            sql_module=fornecedor_item_sql,
            campos_chave=["id_fornecedor", "id_item"],
        )

    def _objeto_para_tupla_insert(self, fornecedor_item: FornecedorItem) -> tuple:
        """Converte objeto FornecedorItem em tupla para INSERT"""
        return (
            fornecedor_item.id_fornecedor,
            fornecedor_item.id_item,
            fornecedor_item.observacoes,
            fornecedor_item.preco_personalizado,
            fornecedor_item.disponivel,
        )

    def _objeto_para_tupla_update(self, fornecedor_item: FornecedorItem) -> tuple:
        """Converte objeto FornecedorItem em tupla para UPDATE"""
        return (
            fornecedor_item.observacoes,
            fornecedor_item.preco_personalizado,
            fornecedor_item.disponivel,
            fornecedor_item.id_fornecedor,
            fornecedor_item.id_item,
        )

    def _linha_para_objeto(self, linha: dict) -> FornecedorItem:
        """Converte linha do banco em objeto FornecedorItem"""
        return FornecedorItem(
            id_fornecedor=linha["id_fornecedor"],
            id_item=linha["id_item"],
            observacoes=linha["observacoes"],
            preco_personalizado=linha["preco_personalizado"],
            disponivel=bool(linha["disponivel"]),
        )

    def obter(self, id_fornecedor: int, id_item: int) -> FornecedorItem:
        """Obtém um relacionamento fornecedor-item específico"""
        return self.obter_por_chave(id_fornecedor, id_item)

    def obter_itens_por_fornecedor(self, id_fornecedor: int) -> List[dict]:
        """Obtém todos os itens de um fornecedor"""
        resultados = self.executar_consulta(
            fornecedor_item_sql.OBTER_ITENS_POR_FORNECEDOR, (id_fornecedor,)
        )
        return [dict(resultado) for resultado in resultados]

    def obter_fornecedores_por_item(self, id_item: int) -> List[dict]:
        """Obtém todos os fornecedores de um item"""
        resultados = self.executar_consulta(
            fornecedor_item_sql.OBTER_FORNECEDORES_POR_ITEM, (id_item,)
        )
        return [dict(resultado) for resultado in resultados]

    def obter_itens_por_fornecedor_e_tipo(
        self, id_fornecedor: int, tipo: TipoFornecimento
    ) -> List[dict]:
        """Obtém itens de um fornecedor filtrados por tipo"""
        resultados = self.executar_consulta(
            fornecedor_item_sql.OBTER_ITENS_POR_FORNECEDOR_E_TIPO,
            (id_fornecedor, tipo.value),
        )
        return [dict(resultado) for resultado in resultados]


# Instância singleton do repositório
fornecedor_item_repo = FornecedorItemRepo()
