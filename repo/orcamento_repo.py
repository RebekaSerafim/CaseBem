from typing import Optional, List
from datetime import datetime
from util.database import obter_conexao
from sql.orcamento_sql import *
from model.orcamento_model import Orcamento

def criar_tabela_orcamento() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de orçamentos
            cursor.execute(CRIAR_TABELA_ORCAMENTO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de orçamentos: {e}")
        # Retorna False indicando falha
        return False

def inserir_orcamento(orcamento: Orcamento) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir orçamento com todos os campos
        cursor.execute(INSERIR_ORCAMENTO, 
            (orcamento.id_demanda, orcamento.id_fornecedor_prestador,
             orcamento.data_hora_cadastro, orcamento.data_hora_validade,
             orcamento.status, orcamento.observacoes, orcamento.valor_total))
        # Retorna o ID do orçamento inserido
        return cursor.lastrowid

def atualizar_orcamento(orcamento: Orcamento) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do orçamento pelo ID
        cursor.execute(ATUALIZAR_ORCAMENTO, 
            (orcamento.data_hora_validade, orcamento.status,
             orcamento.observacoes, orcamento.valor_total, orcamento.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar status do orçamento
        cursor.execute(ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_valor_total_orcamento(id_orcamento: int, valor_total: float) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar valor total do orçamento
        cursor.execute(ATUALIZAR_VALOR_TOTAL_ORCAMENTO, (valor_total, id_orcamento))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para aceitar orçamento e rejeitar outros
        cursor.execute(ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_orcamento(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar orçamento pelo ID
        cursor.execute(EXCLUIR_ORCAMENTO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_orcamento_por_id(id: int) -> Optional[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamento pelo ID
        cursor.execute(OBTER_ORCAMENTO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Orcamento com dados do banco
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
    # Retorna None se não encontrou orçamento
    return None

def obter_orcamentos_por_demanda(id_demanda: int) -> List[Orcamento]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por demanda
        cursor.execute(OBTER_ORCAMENTOS_POR_DEMANDA, (id_demanda,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
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
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por fornecedor/prestador
        cursor.execute(OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR, (id_fornecedor_prestador,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
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
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por noivo
        cursor.execute(OBTER_ORCAMENTOS_POR_NOIVO, (id_noivo,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
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
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos por status
        cursor.execute(OBTER_ORCAMENTOS_POR_STATUS, (status,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
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
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar orçamentos com paginação
        cursor.execute(OBTER_ORCAMENTOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Orcamento a partir dos resultados
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
def aceitar_orcamento_e_rejeitar_outros(id_orcamento: int, id_demanda: int) -> bool:
    """Aceita um orçamento específico e rejeita todos os outros da mesma demanda"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS, (id_orcamento, id_demanda))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao aceitar orçamento: {e}")
        return False

def rejeitar_orcamento(id_orcamento: int) -> bool:
    """Rejeita um orçamento específico"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(REJEITAR_ORCAMENTO, (id_orcamento,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao rejeitar orçamento: {e}")
        return False

def atualizar_status_orcamento(id_orcamento: int, status: str) -> bool:
    """Atualiza o status de um orçamento"""
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(ATUALIZAR_STATUS_ORCAMENTO, (status, id_orcamento))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar status do orçamento: {e}")
        return False
