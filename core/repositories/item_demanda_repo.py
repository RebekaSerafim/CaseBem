from typing import Optional, List
from util.exceptions import RecursoNaoEncontradoError
from util.database import obter_conexao
from core.sql.item_demanda_sql import *
from core.models.item_demanda_model import ItemDemanda

def criar_tabela_item_demanda() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_ITEM_DEMANDA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela item_demanda: {e}")
        return False

def inserir_item_demanda(item_demanda: ItemDemanda) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_ITEM_DEMANDA,
                (item_demanda.id_demanda, item_demanda.id_item,
                 item_demanda.quantidade, item_demanda.observacoes,
                 item_demanda.preco_maximo))
            return True
    except Exception as e:
        print(f"Erro ao inserir item_demanda: {e}")
        return False

def atualizar_item_demanda(item_demanda: ItemDemanda) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_ITEM_DEMANDA,
                (item_demanda.quantidade, item_demanda.observacoes,
                 item_demanda.preco_maximo, item_demanda.id_demanda,
                 item_demanda.id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar item_demanda: {e}")
        return False

def excluir_item_demanda(id_demanda: int, id_item: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_ITEM_DEMANDA, (id_demanda, id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir item_demanda: {e}")
        return False

def obter_item_demanda(id_demanda: int, id_item: int) -> ItemDemanda:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITEM_DEMANDA, (id_demanda, id_item))
            resultado = cursor.fetchone()
            if resultado:
                return ItemDemanda(
                    id_demanda=resultado["id_demanda"],
                    id_item=resultado["id_item"],
                    quantidade=resultado["quantidade"],
                    observacoes=resultado["observacoes"],
                    preco_maximo=resultado["preco_maximo"]
                )
    except Exception as e:
        print(f"Erro ao obter item_demanda: {e}")
        raise
    raise RecursoNaoEncontradoError(recurso="ItemDemanda", identificador=f"{id_demanda}/{id_item}")

def obter_itens_por_demanda(id_demanda: int) -> List[dict]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_DEMANDA, (id_demanda,))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por demanda: {e}")
        return []

def excluir_itens_por_demanda(id_demanda: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_ITENS_POR_DEMANDA, (id_demanda,))
            return True
    except Exception as e:
        print(f"Erro ao excluir itens por demanda: {e}")
        return False