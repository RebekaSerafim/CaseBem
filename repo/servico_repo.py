from typing import Optional
from util.database import obter_conexao
from sql.servico_sql import *
from model.servico_model import Servico

def criar_tabela_servicos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(criar_tabela_servicos)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de serviços: {e}")
        # Retorna False indicando falha
        return False

def inserir_servico(servico: Servico) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir serviço com todos os campos
        cursor.execute(INSERIR_SERVICO, 
            (servico.nome, servico.preco, servico.descricao))
        # Retorna o ID do serviço inserido
        return cursor.lastrowid        

def atualizar_servico(servico: Servico) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do serviço pelo ID
        cursor.execute(ATUALIZAR_SERVICO, 
            (servico.nome, servico.preco, servico.descricao, servico.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_tipo_servico(id: int, tipo: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar tipo do usuário (0=comum, 1=admin)
        cursor.execute(ATUALIZAR_TIPO_SERVICO, (tipo, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_servico(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_SERVICO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_servico_por_id(id: int) -> Optional[Servico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar serviço pelo ID
        cursor.execute(OBTER_SERVICO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Servico com dados do banco
            return Servico(
                id=resultado["id"],
                nome=resultado["nome"],
                preco=resultado["preco"],
                descricao=resultado["descricao"]
            )
    # Retorna None se não encontrou serviço
    return None


    # Retorna None se não encontrou usuário
    return None

def obter_servicos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Servico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar serviços com paginação
        cursor.execute(obter_servicos_por_pagina, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Servico a partir dos resultados
        return [Servico(
            id=resultado["id"],
            nome=resultado["nome"],
            preco=resultado["preco"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou serviços
    return []