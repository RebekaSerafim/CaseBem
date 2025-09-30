from typing import Optional, List
from util.exceptions import RecursoNaoEncontradoError
from util.database import obter_conexao
from core.sql.item_orcamento_sql import *
from core.models.item_orcamento_model import ItemOrcamento

def criar_tabela_item_orcamento() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_ITEM_ORCAMENTO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela item_orcamento: {e}")
        return False

def inserir_item_orcamento(item_orcamento: ItemOrcamento) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(INSERIR_ITEM_ORCAMENTO,
                (item_orcamento.id_orcamento, item_orcamento.id_item,
                 item_orcamento.quantidade, item_orcamento.preco_unitario,
                 item_orcamento.observacoes, item_orcamento.desconto))
            return True
    except Exception as e:
        print(f"Erro ao inserir item_orcamento: {e}")
        return False

def atualizar_item_orcamento(item_orcamento: ItemOrcamento) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_ITEM_ORCAMENTO,
                (item_orcamento.quantidade, item_orcamento.preco_unitario,
                 item_orcamento.observacoes, item_orcamento.desconto,
                 item_orcamento.id_orcamento, item_orcamento.id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar item_orcamento: {e}")
        return False

def excluir_item_orcamento(id_orcamento: int, id_item: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_ITEM_ORCAMENTO, (id_orcamento, id_item))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir item_orcamento: {e}")
        return False

def obter_item_orcamento(id_orcamento: int, id_item: int) -> ItemOrcamento:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITEM_ORCAMENTO, (id_orcamento, id_item))
            resultado = cursor.fetchone()
            if resultado:
                return ItemOrcamento(
                    id_orcamento=resultado["id_orcamento"],
                    id_item=resultado["id_item"],
                    quantidade=resultado["quantidade"],
                    preco_unitario=resultado["preco_unitario"],
                    observacoes=resultado["observacoes"],
                    desconto=resultado["desconto"]
                )
    except Exception as e:
        print(f"Erro ao obter item_orcamento: {e}")
        raise
    raise RecursoNaoEncontradoError(recurso="ItemOrcamento", identificador=f"{id_orcamento}/{id_item}")

def obter_itens_por_orcamento(id_orcamento: int) -> List[dict]:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,))
            resultados = cursor.fetchall()
            return [dict(resultado) for resultado in resultados]
    except Exception as e:
        print(f"Erro ao obter itens por orçamento: {e}")
        return []

def obter_total_orcamento(id_orcamento: int) -> float:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(OBTER_TOTAL_ORCAMENTO, (id_orcamento,))
            resultado = cursor.fetchone()
            return resultado["total"] if resultado and resultado["total"] else 0.0
    except Exception as e:
        print(f"Erro ao obter total do orçamento: {e}")
        return 0.0

def excluir_itens_por_orcamento(id_orcamento: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(EXCLUIR_ITENS_POR_ORCAMENTO, (id_orcamento,))
            return True
    except Exception as e:
        print(f"Erro ao excluir itens por orçamento: {e}")
        return False