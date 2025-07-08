from typing import Optional, List
from util.database import obter_conexao
from sql.item_demanda_produto_sql import *
from model.item_demanda_produto_model import ItemDemandaProduto

def criar_tabela_item_demanda_produto() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_ITEM_DEMANDA_PRODUTO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela ItemDemandaProduto: {e}")
        return False

def inserir_item_demanda_produto(item: ItemDemandaProduto) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_ITEM_DEMANDA_PRODUTO,
            (item.id_demanda, item.id_produto, item.quantidade, item.observacoes)
        )
        return cursor.rowcount > 0

def atualizar_item_demanda_produto(item: ItemDemandaProduto) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_ITEM_DEMANDA_PRODUTO,
            (item.quantidade, item.observacoes, item.id_demanda, item.id_produto)
        )
        return cursor.rowcount > 0

def excluir_item_demanda_produto(id_demanda: int, id_produto: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_ITEM_DEMANDA_PRODUTO, (id_demanda, id_produto))
        return cursor.rowcount > 0

def obter_item_demanda_produto_por_id(id_demanda: int, id_produto: int) -> Optional[ItemDemandaProduto]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITEM_DEMANDA_PRODUTO_POR_ID, (id_demanda, id_produto))
        row = cursor.fetchone()
        if row:
            return ItemDemandaProduto(
                id_demanda=row["id_demanda"],
                id_produto=row["id_produto"],
                quantidade=row["quantidade"],
                observacoes=row["observacoes"]
            )
    return None

def obter_itens_por_demanda(id_demanda: int) -> List[ItemDemandaProduto]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_POR_DEMANDA, (id_demanda,))
        rows = cursor.fetchall()
        return [
            ItemDemandaProduto(
                id_demanda=row["id_demanda"],
                id_produto=row["id_produto"],
                quantidade=row["quantidade"],
                observacoes=row["observacoes"]
            ) for row in rows
        ]

def obter_itens_demanda_produto_por_pagina(pagina: int, tamanho: int) -> List[ItemDemandaProduto]:
    offset = (pagina - 1) * tamanho
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_ITENS_DEMANDA_PRODUTO_POR_PAGINA, (tamanho, offset))
        rows = cursor.fetchall()
        return [
            ItemDemandaProduto(
                id_demanda=row["id_demanda"],
                id_produto=row["id_produto"],
                quantidade=row["quantidade"],
                observacoes=row["observacoes"]
            ) for row in rows
        ]