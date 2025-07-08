from typing import Optional, List
from datetime import datetime
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
            (demanda.id_casal, demanda.data_hora_cadastro))
        # Retorna o ID da demanda inserida
        return cursor.lastrowid

def atualizar_demanda(demanda: Demanda) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados da demanda pelo ID
        cursor.execute(ATUALIZAR_DEMANDA, 
            (demanda.id_casal, demanda.data_hora_cadastro, demanda.id))    
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
            # Cria e retorna objeto Demanda com dados do banco
            return Demanda(
                id=resultado["id"],
                id_casal=resultado["id_casal"],
                data_hora_cadastro=resultado["data_hora_cadastro"])
    # Retorna None se não encontrou demanda
    return None

def obter_demandas_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[Demanda]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar demandas com paginação
        cursor.execute(OBTER_DEMANDAS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Demanda a partir dos resultados
        return [Demanda(
            id=resultado["id"],
            id_casal=resultado["id_casal"],
            data_hora_cadastro=resultado["data_hora_cadastro"]
        ) for resultado in resultados]

def obter_demandas_por_casal(id_casal: int) -> List[Demanda]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar demandas por casal
        cursor.execute(OBTER_DEMANDAS_POR_CASAL, (id_casal,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Demanda a partir dos resultados
        return [Demanda(
            id=resultado["id"],
            id_casal=resultado["id_casal"],
            data_hora_cadastro=resultado["data_hora_cadastro"]
        ) for resultado in resultados]