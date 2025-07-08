from typing import Optional, List
from util.database import obter_conexao
from sql.item_orcamento_servico_sql import *
from model.item_orcamento_servico_model import ItemOrcamentoServico

def criar_tabela_item_orcamento_servico() -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para criar tabela de itens de orçamento serviço
            cursor.execute(CRIAR_TABELA_ITEM_ORCAMENTO_SERVICO)
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao criar tabela de itens de orçamento serviço: {e}")
        # Retorna False indicando falha
        return False

def inserir_item_orcamento_servico(item: ItemOrcamentoServico) -> bool:
    try:
        # Obtém conexão com o banco de dados
        with obter_conexao() as conexao:
            # Cria cursor para executar comandos SQL
            cursor = conexao.cursor()
            # Executa comando SQL para inserir item com todos os campos
            cursor.execute(INSERIR_ITEM_ORCAMENTO_SERVICO, 
                (item.id_orcamento, item.id_servico, 
                 item.preco_unitario, item.quantidade, item.observacoes))
            # Retorna True indicando sucesso
            return True
    except Exception as e:
        # Imprime mensagem de erro caso ocorra exceção
        print(f"Erro ao inserir item de orçamento serviço: {e}")
        # Retorna False indicando falha
        return False

def atualizar_item_orcamento_servico(item: ItemOrcamentoServico) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para atualizar dados do item pela chave composta
        cursor.execute(ATUALIZAR_ITEM_ORCAMENTO_SERVICO, 
            (item.preco_unitario, item.quantidade, item.observacoes,
             item.id_orcamento, item.id_servico))    
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def excluir_item_orcamento_servico(id_orcamento: int, id_servico: int) -> bool:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para deletar item pela chave composta
        cursor.execute(EXCLUIR_ITEM_ORCAMENTO_SERVICO, (id_orcamento, id_servico))
        # Retorna True se alguma linha foi afetada
        return (cursor.rowcount > 0)

def obter_item_orcamento_servico_por_id(id_orcamento: int, id_servico: int) -> Optional[ItemOrcamentoServico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar item pela chave composta
        cursor.execute(OBTER_ITEM_ORCAMENTO_SERVICO_POR_ID, (id_orcamento, id_servico))
        # Obtém primeiro resultado da consulta
        resultado = cursor.fetchone()
        # Verifica se encontrou resultado
        if resultado:
            # Cria e retorna objeto ItemOrcamentoServico com dados do banco
            return ItemOrcamentoServico(
                id_orcamento=resultado["id_orcamento"],
                id_servico=resultado["id_servico"],
                preco_unitario=resultado["preco_unitario"],
                quantidade=resultado["quantidade"],
                observacoes=resultado["observacoes"]
            )
    # Retorna None se não encontrou item
    return None

def obter_itens_por_orcamento(id_orcamento: int) -> List[ItemOrcamentoServico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar itens por orçamento
        cursor.execute(OBTER_ITENS_POR_ORCAMENTO, (id_orcamento,))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos ItemOrcamentoServico a partir dos resultados
        return [ItemOrcamentoServico(
            id_orcamento=resultado["id_orcamento"],
            id_servico=resultado["id_servico"],
            preco_unitario=resultado["preco_unitario"],
            quantidade=resultado["quantidade"],
            observacoes=resultado["observacoes"]
        ) for resultado in resultados]

def obter_itens_orcamento_servico_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[ItemOrcamentoServico]:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Define limite de registros por página
        limite = tamanho_pagina
        # Calcula offset baseado no número da página
        offset = (numero_pagina - 1) * tamanho_pagina
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para buscar itens com paginação
        cursor.execute(OBTER_ITENS_ORCAMENTO_SERVICO_POR_PAGINA, (limite, offset))
        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()
        # Cria lista de objetos ItemOrcamentoServico a partir dos resultados
        return [ItemOrcamentoServico(
            id_orcamento=resultado["id_orcamento"],
            id_servico=resultado["id_servico"],
            preco_unitario=resultado["preco_unitario"],
            quantidade=resultado["quantidade"],
            observacoes=resultado["observacoes"]
        ) for resultado in resultados]

def calcular_total_itens_servico_orcamento(id_orcamento: int) -> float:
    # Obtém conexão com o banco de dados
    with obter_conexao() as conexao:
        # Cria cursor para executar comandos SQL
        cursor = conexao.cursor()
        # Executa comando SQL para calcular total
        cursor.execute(CALCULAR_TOTAL_ITENS_SERVICO_ORCAMENTO, (id_orcamento,))
        # Obtém resultado
        resultado = cursor.fetchone()
        # Retorna o total ou 0 se não houver itens
        return resultado["total"] if resultado["total"] else 0.0