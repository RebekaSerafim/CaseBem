from typing import Optional
from util.database import obter_conexao
from sql.usuario_sql import *
from model.usuario_model import TipoUsuario, Usuario

def criar_tabela_usuarios() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de usuários
            cursor.execute(CRIAR_TABELA_USUARIO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de usuários: {e}")
        # Retorna False indicando falha
        return False
   

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir usuário com todos os campos
        cursor.execute(INSERIR_USUARIO,
            (usuario.nome, usuario.telefone, usuario.email, usuario.senha, usuario.perfil.value))
        # Retorna o ID do usuário inserido
        return cursor.lastrowid        

def atualizar_usuario(usuario: Usuario) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do usuário pelo ID
        cursor.execute(ATUALIZAR_USUARIO,
            (usuario.nome, usuario.telefone, usuario.email, usuario.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    
def atualizar_senha_usuario(id: int, senha_hash: str) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar senha do usuário
        cursor.execute(ATUALIZAR_SENHA_USUARIO, (senha_hash, id))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_usuario(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar usuário pelo ID
        cursor.execute(EXCLUIR_USUARIO, (id,))
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
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"])
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
                senha=resultado["senha"],
                perfil=TipoUsuario(resultado["perfil"]),
                foto=resultado["foto"],
                token_redefinicao=resultado["token_redefinicao"],
                data_token=resultado["data_token"],
                data_cadastro=resultado["data_cadastro"])
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
            senha=resultado["senha"],
            perfil=TipoUsuario(resultado["perfil"]),
            foto=resultado["foto"],
            token_redefinicao=resultado["token_redefinicao"],
            data_token=resultado["data_token"],
            data_cadastro=resultado["data_cadastro"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []


def obter_usuarios_por_tipo_por_pagina(tipo: TipoUsuario, numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar usuários por tipo com paginação
        cursor.execute(OBTER_USUARIOS_POR_TIPO_POR_PAGINA, (tipo.value, limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Usuario a partir dos resultados
        return [Usuario(
            id=resultado["id"],
            nome=resultado["nome"],
            telefone=resultado["telefone"],
            email=resultado["email"],
            senha=resultado["senha"],
            perfil=TipoUsuario(resultado["perfil"]),
            foto=resultado["foto"],
            token_redefinicao=resultado["token_redefinicao"],
            data_token=resultado["data_token"],
            data_cadastro=resultado["data_cadastro"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou usuários
    return []