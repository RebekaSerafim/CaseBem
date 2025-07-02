from typing import Optional
from util.database import obter_conexao
from sql.contrato_sql import *
from model.contrato_model import contrato

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

def atualizar_senha_contrato(id: int, senha_hash: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar senha hash do contrato
        cursor.execute(ATUALIZAR_SENHA_CONTRATO, (senha_hash, id))
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

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo ID
        cursor.execute(OBTER_USUARIO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuário pelo email
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Usuario com dados do banco
            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                telefone=resultado["telefone"],
                email=resultado["email"],
                senha_hash=resultado["senha_hash"],
                tipo=resultado["tipo"])
    # Retorna None se não encontrou usuário
    return None

def obter_usuarios_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários com paginação
        cursor.execute(OBTER_USUARIOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            tipo=resultado["tipo"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []