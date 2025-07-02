from typing import Optional
from repo import usuario_repo
from repo import prestador_repo
from util.database import obter_conexao
from sql.prestador_sql import *
from model.prestador_model import Prestador

def criar_tabela_prestadores() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CRIAR_TABELA_PRESTADOR)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de usuários: {e}")
        # Retorna False indicando falha
        return False

def inserir_prestador(prestador: Prestador) -> Optional[int]:
    # Tenta inserir o prestador no repositório de prestadores
    id_prestador = usuario_repo.inserir_usuario(prestador)
    # Verifica se o usuário foi inserido com sucesso
    if id_prestador is None:
        # Retorna None se não conseguiu inserir o usuário
        return None
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir prestador com todos os campos
        cursor.execute(INSERIR_PRESTADOR, 
            (id_prestador, prestador.tipo_pessoa, prestador.documento))
        # Retorna o ID do prestador inserido
        return cursor.lastrowid        

def atualizar_prestador(prestador: Prestador) -> bool:
    # Tenta atualizar o usuário no repositório de usuários
    if not usuario_repo.atualizar_prestador(prestador):
        # Retorna False se não conseguiu atualizar o usuário
        return False
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_PRESTADOR, 
            (prestador.tipo_pessoa, prestador.documento, prestador.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def excluir_prestador(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_PRESTADOR, (id,))
        # Tenta excluir o usuário no repositório de usuários
        usuario_excluido = usuario_repo.excluir_prestador(id)
        # Verifica se o usuário foi excluído com sucesso
        if not usuario_excluido:
            # Retorna False se não conseguiu excluir o usuário
            return False
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_prestador_por_id(id: int) -> Optional[Prestador]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(OBTER_PRESTADOR_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Prestador com dados do banco
            return Prestador(
                id=resultado["id_prestador"],
                nome=resultado["nome"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"],
                tipo_pessoa=resultado["tipo_pessoa"],
                documento=resultado["documento"]
            )
    # Retorna None se não encontrou usuário
    return None

def obter_prestadores_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Prestador]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(OBTER_PRESTADORES_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Prestador a partir dos resultados
        return [Prestador(
            id=resultado["id_prestador"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            senha_hash=resultado["senha_hash"],
            tipo=resultado["tipo"],
            tipo_pessoa=resultado["tipo_pessoa"],
            documento=resultado["documento"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []