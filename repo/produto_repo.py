from typing import Optional
from util.database import obter_conexao
from sql.produto_sql import *
from model.produto_model import Produto

def criar_tabela_produtos() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de produtos
            cursor.execute(CRIAR_TABELA_PRODUTO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de produtos: {e}")
        # Retorna False indicando falha
        return False

def inserir_produto(produto: Produto) -> Optional[int]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para inserir produto com todos os campos
        cursor.execute(INSERIR_PRODUTO, 
            (produto.nome, produto.preco, produto.quantidade, produto.descricao))
        # Retorna o ID do produto inserido
        return cursor.lastrowid        

def atualizar_produto(produto: Produto) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do produto pelo ID
        cursor.execute(ATUALIZAR_PRODUTO, 
            (produto.nome, produto.preco, produto.quantidade, produto.descricao, produto.id))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)
    

def excluir_produto(id: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar produto pelo ID
        cursor.execute(EXCLUIR_PRODUTO, (id,))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)    

def obter_produto_por_id(id: int) -> Optional[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produto pelo ID
        cursor.execute(OBTER_PRODUTO_POR_ID, (id,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Produto com dados do banco
            return Produto(
                id=resultado["id"],
                nome=resultado["nome"],
                preco=resultado["preco"],
                quantidade=resultado["quantidade"],
                descricao=resultado["descricao"])
    # Retorna None se não encontrou produto
    return None

def obter_produto_por_nome(nome: str) -> Optional[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produto pelo nome
        cursor.execute(OBTER_PRODUTO_POR_NOME, (nome,))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto Produto com dados do banco
            return Produto(
                id=resultado["id"],
                nome=resultado["nome"],
                preco=resultado["preco"],
                quantidade=resultado["quantidade"],
                descricao=resultado["descricao"])
    # Retorna None se não encontrou produto
    return None

def obter_produtos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Produto]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar produtos com paginação
        cursor.execute(OBTER_PRODUTOS_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos Produto a partir dos resultados
        return [Produtoo(
            id=resultado["id"],
            nome=resultado["nome"],
            preco=resultado["preco"],
            quantidade=resultado["quantidade"],
            descricao=resultado["descricao"]
        ) for resultado in resultados]
    # Retorna lista vazia se não encontrou produtos
    return []