from typing import Optional, List
from util.database import obter_conexao
from sql.item_contrato_produto_sql import *
from model.item_contrato_produto_model import ItemContratoProduto

def criar_tabela_item_contrato_produto() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM_CONTRATO_PRODUTO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela ItemContratoProduto: {e}")
        return False

def inserir_item_contrato_produto(item: ItemContratoProduto) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_ITEM_CONTRATO_PRODUTO,
            (item.valor, item.quantidade, item.id_produto)
        )
        return cursor.lastrowid

def atualizar_item_contrato_produto(item: ItemContratoProduto) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_ITEM_CONTRATO_PRODUTO,
            (item.valor, item.quantidade, item.id_produto, item.id_item_contrato_produto)
        )
        return cursor.rowcount > 0

def excluir_item_contrato_produto(id_item: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_ITEM_CONTRATO_PRODUTO, (id_item,))
        return cursor.rowcount > 0

def obter_item_contrato_produto_por_id(id_item: int) -> Optional[ItemContratoProduto]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITEM_CONTRATO_PRODUTO_POR_ID, (id_item,))
        row = cursor.fetchone()
        if row:
            return ItemContratoProduto(
                id_item_contrato_produto=row["idItemContratoProduto"],
                valor=row["valor"],
                quantidade=row["quantidade"],
                id_produto=row["idProduto"]
            )
    return None

def obter_itens_contrato_produto(pagina: int, tamanho: int) -> List[ItemContratoProduto]:
    offset = (pagina - 1) * tamanho
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_CONTRATO_PRODUTO, (tamanho, offset))
        rows = cursor.fetchall()
        return [
            ItemContratoProduto(
                id_item_contrato_produto=row["idItemContratoProduto"],
                valor=row["valor"],
                quantidade=row["quantidade"],
                id_produto=row["idProduto"]
            ) for row in rows
        ]
