from typing import Optional
from util.database import obter_conexao
from sql.demanda_sql import *
from model.demanda_model import Demanda

def criar_tabela_demandas() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de demandas
            cursor.execute(CRIAR_TABELA_DEMANDA)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de demandas: {e}")
        # Retorna False indicando falha
        return False

def inserir_demanda(demanda: Demanda) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir demanda com todos os campos
        cursor.execute(INSERIR_DEMANDA, 
            (demanda.valor,))
        # Retorna o ID do demanda inserido
        return cursor.lastrowid

def atualizar_demanda(demanda: Demanda) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do demanda pelo ID
        cursor.execute(ATUALIZAR_DEMANDA, 
            (demanda.valor, demanda.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def atualizar_tipo_demanda(id: int, tipo: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do demanda (0=serviço, 1=produto)
        cursor.execute(ATUALIZAR_TIPO_DEMANDA, (tipo, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)


def excluir_demanda(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar demanda pelo ID
        cursor.execute(EXCLUIR_DEMANDA, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_demanda_por_id(id: int) -> Optional[Demanda]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar demanda pelo ID
        cursor.execute(OBTER_DEMANDA_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Contrato com dados do banco
            return Demanda(
                id=resultado["id"],
                valor=resultado["valor"])
    # Retorna None se não encontrou usuário
    return None