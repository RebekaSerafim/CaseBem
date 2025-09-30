from typing import Optional, List
from util.exceptions import RecursoNaoEncontradoError
from datetime import datetime
from util.database import obter_conexao
from core.sql.orcamento_sql import *
from core.models.orcamento_model import Orcamento

def criar_tabela_orcamento() -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(CRIAR_TABELA_ORCAMENTO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de orçamentos: {e}")
        return False

def inserir_orcamento(orcamento: Orcamento) -> Optional[int]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(INSERIR_ORCAMENTO,
            (orcamento.id_demanda, orcamento.id_fornecedor_prestador,
             orcamento.data_hora_cadastro, orcamento.data_hora_validade,
             orcamento.status, orcamento.observacoes, orcamento.valor_total))
        return cursor.lastrowid

def atualizar_orcamento(orcamento: Orcamento) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_ORCAMENTO,
            (orcamento.data_hora_validade, orcamento.status,
             orcamento.observacoes, orcamento.valor_total, orcamento.id))
        return (cursor.rowcount > 0)

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar status do orçamento: {e}")
        return False

def atualizar_valor_total_orcamento(id_orcamento: int, valor_total: float) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento))
        return (cursor.rowcount > 0)

def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao aceitar orçamento: {e}")
        return False

def rejeitar_orcamento(id_orcamento: int) -> bool:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(REJEITAR_ORCAMENTO, (id_orcamento,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao rejeitar orçamento: {e}")
        return False

def excluir_orcamento(id: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(EXCLUIR_ORCAMENTO, (id,))
        return (cursor.rowcount > 0)

def obter_orcamento_por_id(id: int) -> Orcamento:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_ORCAMENTO_POR_ID, (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Orcamento(
                id=resultado["id"],
                id_demanda=resultado["id_demanda"],
                id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
                data_hora_cadastro=resultado["data_hora_cadastro"],
                data_hora_validade=resultado["data_hora_validade"],
                status=resultado["status"],
                observacoes=resultado["observacoes"],
                valor_total=resultado["valor_total"]
            )
    raise RecursoNaoEncontradoError(recurso="Orcamento", identificador=id)

def obter_orcamentos_por_demanda(id_demanda: int) -> List[Orcamento]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
        resultados = cursor.fetchall()
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_fornecedor_prestador(id_fornecedor_prestador: int) -> List[Orcamento]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR, (id_fornecedor_prestador,))
        resultados = cursor.fetchall()
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_noivo(id_noivo: int) -> List[Orcamento]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo,))
        resultados = cursor.fetchall()
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_status(status: str) -> List[Orcamento]:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(OBTER_ORCAMENTOS_POR_STATUS, (status,))
        resultados = cursor.fetchall()
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def obter_orcamentos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Orcamento]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.cursor()
        cursor.execute(OBTER_ORCAMENTOS_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [Orcamento(
            id=resultado["id"],
            id_demanda=resultado["id_demanda"],
            id_fornecedor_prestador=resultado["id_fornecedor_prestador"],
            data_hora_cadastro=resultado["data_hora_cadastro"],
            data_hora_validade=resultado["data_hora_validade"],
            status=resultado["status"],
            observacoes=resultado["observacoes"],
            valor_total=resultado["valor_total"]
        ) for resultado in resultados]

def contar_orcamentos() -> int:
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM orcamento")
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
    except Exception as e:
        print(f"Erro ao contar orçamentos: {e}")
        return 0