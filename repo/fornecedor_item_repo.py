from typing import Optional, List
from util.base_repo import BaseRepoChaveComposta
from sql import fornecedor_item_sql
from model.fornecedor_item_model import FornecedorItem
from model.tipo_fornecimento_model import TipoFornecimento

class FornecedorItemRepo(BaseRepoChaveComposta):
    """Repositório para operações com fornecedor_item (chave composta)"""

    def __init__(self):
        # FornecedorItem tem chave composta: (id_fornecedor, id_item)
        super().__init__('fornecedor_item', FornecedorItem, fornecedor_item_sql, ['id_fornecedor', 'id_item'])

    def _objeto_para_tupla_insert(self, fornecedor_item: FornecedorItem) -> tuple:
        """Prepara dados do fornecedor_item para inserção"""
        return (
            fornecedor_item.id_fornecedor,
            fornecedor_item.id_item,
            fornecedor_item.observacoes,
            fornecedor_item.preco_personalizado,
            fornecedor_item.disponivel
        )

    def _objeto_para_tupla_update(self, fornecedor_item: FornecedorItem) -> tuple:
        """Prepara dados do fornecedor_item para atualização"""
        return (
            fornecedor_item.observacoes,
            fornecedor_item.preco_personalizado,
            fornecedor_item.disponivel,
            fornecedor_item.id_fornecedor,
            fornecedor_item.id_item
        )

    def _linha_para_objeto(self, linha: dict) -> FornecedorItem:
        """Converte linha do banco em objeto FornecedorItem"""
        return FornecedorItem(
            id_fornecedor=linha["id_fornecedor"],
            id_item=linha["id_item"],
            observacoes=linha.get("observacoes"),
            preco_personalizado=linha.get("preco_personalizado"),
            disponivel=bool(linha.get("disponivel", True))
        )

    def obter_itens_por_fornecedor(self, id_fornecedor: int) -> List[dict]:
        """Obtém todos os itens de um fornecedor com dados dos itens"""
        resultados = self.executar_query(fornecedor_item_sql.OBTER_ITENS_POR_FORNECEDOR, (id_fornecedor,))
        return [dict(resultado) for resultado in resultados]

    def obter_fornecedores_por_item(self, id_item: int) -> List[dict]:
        """Obtém todos os fornecedores de um item com dados dos fornecedores"""
        resultados = self.executar_query(fornecedor_item_sql.OBTER_FORNECEDORES_POR_ITEM, (id_item,))
        return [dict(resultado) for resultado in resultados]

    def obter_itens_por_fornecedor_e_tipo(self, id_fornecedor: int, tipo: TipoFornecimento) -> List[dict]:
        """Obtém itens de um fornecedor por tipo de fornecimento"""
        resultados = self.executar_query(fornecedor_item_sql.OBTER_ITENS_POR_FORNECEDOR_E_TIPO, (id_fornecedor, tipo.value))
        return [dict(resultado) for resultado in resultados]

# Instância global do repositório
fornecedor_item_repo = FornecedorItemRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_fornecedor_item() -> bool:
    return fornecedor_item_repo.criar_tabela()

def inserir_fornecedor_item(fornecedor_item: FornecedorItem) -> bool:
    return fornecedor_item_repo.inserir(fornecedor_item)

def atualizar_fornecedor_item(fornecedor_item: FornecedorItem) -> bool:
    return fornecedor_item_repo.atualizar(fornecedor_item)

def excluir_fornecedor_item(id_fornecedor: int, id_item: int) -> bool:
    return fornecedor_item_repo.excluir(id_fornecedor, id_item)

def obter_fornecedor_item(id_fornecedor: int, id_item: int) -> Optional[FornecedorItem]:
    return fornecedor_item_repo.obter_por_chave(id_fornecedor, id_item)

def obter_itens_por_fornecedor(id_fornecedor: int) -> List[dict]:
    return fornecedor_item_repo.obter_itens_por_fornecedor(id_fornecedor)

def obter_fornecedores_por_item(id_item: int) -> List[dict]:
    return fornecedor_item_repo.obter_fornecedores_por_item(id_item)

def obter_itens_por_fornecedor_e_tipo(id_fornecedor: int, tipo: TipoFornecimento) -> List[dict]:
    return fornecedor_item_repo.obter_itens_por_fornecedor_e_tipo(id_fornecedor, tipo)