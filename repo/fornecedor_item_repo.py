from typing import Optional, List
from util.database import obter_conexao
from sql.fornecedor_item_sql import *
from model.fornecedor_item_model import FornecedorItem
from model.item_model import TipoItem

def criar_tabela_fornecedor_item() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_FORNECEDOR_ITEM)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela fornecedor_item: {e}")
        return False

def inserir_fornecedor_item(fornecedor_item: FornecedorItem) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_FORNECEDOR_ITEM,
                (fornecedor_item.id_fornecedor, fornecedor_item.id_item,
                 fornecedor_item.observacoes, fornecedor_item.preco_personalizado,
                 fornecedor_item.disponivel))
            return True
    except Exception as e:
        print(f"Erro ao inserir fornecedor_item: {e}")
        return False

def atualizar_fornecedor_item(fornecedor_item: FornecedorItem) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_FORNECEDOR_ITEM,
                (fornecedor_item.observacoes, fornecedor_item.preco_personalizado,
                 fornecedor_item.disponivel, fornecedor_item.id_fornecedor,
                 fornecedor_item.id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar fornecedor_item: {e}")
        return False

def excluir_fornecedor_item(id_fornecedor: int, id_item: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_FORNECEDOR_ITEM, (id_fornecedor, id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir fornecedor_item: {e}")
        return False

def obter_fornecedor_item(id_fornecedor: int, id_item: int) -> Optional[FornecedorItem]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_FORNECEDOR_ITEM, (id_fornecedor, id_item))
            resultado = cursor.fetchone()
            if resultado:
                return FornecedorItem(
                    id_fornecedor=resultado["id_fornecedor"],
                    id_item=resultado["id_item"],
                    observacoes=resultado["observacoes"],
                    preco_personalizado=resultado["preco_personalizado"],
                    disponivel=bool(resultado["disponivel"])
                )
    except Exception as e:
        print(f"Erro ao obter fornecedor_item: {e}")
    return None

def obter_itens_por_fornecedor(id_fornecedor: int) -> List[dict]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_FORNECEDOR, (id_fornecedor,))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por fornecedor: {e}")
        return []

def obter_fornecedores_por_item(id_item: int) -> List[dict]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_FORNECEDORES_POR_ITEM, (id_item,))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter fornecedores por item: {e}")
        return []

def obter_itens_por_fornecedor_e_tipo(id_fornecedor: int, tipo: TipoItem) -> List[dict]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_FORNECEDOR_E_TIPO, (id_fornecedor, tipo.value))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por fornecedor e tipo: {e}")
        return []