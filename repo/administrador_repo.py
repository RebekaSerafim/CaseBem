from typing import Optional
from repo import usuario_repo
from repo import administrador_repo
from util.database import obter_conexao
from sql.administrador_sql import *
from model.administrador_model import Administrador

def criar_tabela_administradores() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CRIAR_TABELA_ADMINISTRADOR)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de administradores: {e}")
        # Retorna False indicando falha
        return False

def inserir_administrador(administrador: Administrador) -> Optional[int]:
    # Tenta inserir o prestador no repositório de administradores
    id_administrador = usuario_repo.inserir_usuario(administrador)
    # Verifica se o usuário foi inserido com sucesso
    if id_administrador is None:
        # Retorna None se não conseguiu inserir o usuário
        return None
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir administrador com todos os campos
        cursor.execute(INSERIR_ADMINISTRADOR, 
            (id_administrador))
        # Retorna o ID do administrador inserido
        return cursor.lastrowid        

def atualizar_administrador(administrador: Administrador) -> bool:
    # Tenta atualizar o usuário no repositório de usuários
    if not usuario_repo.atualizar_administrador(administrador):
        # Retorna False se não conseguiu atualizar o usuário
        return False
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_ADMINISTRADOR, 
            (administrador.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def excluir_administrador(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_ADMINISTRADOR, (id,))
        # Tenta excluir o usuário no repositório de usuários
        usuario_excluido = usuario_repo.excluir_administrador(id)
        # Verifica se o usuário foi excluído com sucesso
        if not usuario_excluido:
            # Retorna False se não conseguiu excluir o usuário
            return False
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_administrador_por_id(id: int) -> Optional[Administrador]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(OBTER_ADMINISTRADOR_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Administrador com dados do banco
            return Administrador(
                id=resultado["id_administrador"],
                nome=resultado["nome"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"],
            )
    # Retorna None se não encontrou usuário
    return None

def obter_administradores_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Administrador]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(OBTER_ADMINISTRADORES_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Prestador a partir dos resultados
        return [Administrador(
            id=resultado["id_administrador"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            senha_hash=resultado["senha_hash"],
            tipo=resultado["tipo"],
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []