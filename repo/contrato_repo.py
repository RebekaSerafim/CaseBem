from typing import Optional
from util.database import obter_conexao
from sql.contrato_sql import *
from model.contrato_model import Contrato

def criar_tabela_contratos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de contratos
            cursor.execute(CRIAR_TABELA_CONTRATO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de contratos: {e}")
        # Retorna False indicando falha
        return False

def inserir_contrato(contrato: Contrato) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir contrato com todos os campos
        cursor.execute(INSERIR_CONTRATO, 
            (contrato.valor,))
        # Retorna o ID do contrato inserido
        return cursor.lastrowid

def atualizar_contrato(contrato: Contrato) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do contrato pelo ID
        cursor.execute(ATUALIZAR_CONTRATO, 
            (contrato.valor, contrato.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_tipo_contrato(id: int, tipo: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do contrato (0=serviço, 1=produto)
        cursor.execute(ATUALIZAR_TIPO_CONTRATO, (tipo, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)


def excluir_contrato(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar contrato pelo ID
        cursor.execute(EXCLUIR_CONTRATO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_contrato_por_id(id: int) -> Optional[Contrato]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar contrato pelo ID
        cursor.execute(OBTER_CONTRATO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Contrato com dados do banco
            return Contrato(
                id=resultado["id"],
                valor=resultado["valor"]
    # Retorna None se não encontrou usuário
    return None
            )