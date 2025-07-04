from typing import Optional, List
from util.database import obter_conexao
from sql.fornecedor_produto_sql import *
from model.fornecedor_produto_model import FornecedorProduto

def criar_tabela_fornecedor_produto() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_FORNECEDOR_PRODUTO)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela FornecedorProduto: {e}")
        return False

def inserir_fornecedor_produto(fp: FornecedorProduto) -> Optional[tuple]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            INSERIR_FORNECEDOR_PRODUTO,
            (fp.id_fornecedor, fp.id_produto, fp.observacoes, fp.preco)
        )
        return (fp.id_fornecedor, fp.id_produto)

def atualizar_fornecedor_produto(fp: FornecedorProduto) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_FORNECEDOR_PRODUTO,
            (fp.observacoes, fp.preco, fp.id_fornecedor, fp.id_produto)
        )
        return cursor.rowcount > 0

def excluir_fornecedor_produto(id_fornecedor: int, id_produto: int) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(EXCLUIR_FORNECEDOR_PRODUTO, (id_fornecedor, id_produto))
        return cursor.rowcount > 0

def obter_fornecedor_produto_por_id(id_fornecedor: int, id_produto: int) -> Optional[FornecedorProduto]:
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_FORNECEDOR_PRODUTO_POR_ID, (id_fornecedor, id_produto))
        resultado = cursor.fetchone()
        if resultado:
            return FornecedorProduto(
                id_fornecedor=resultado["idFornecedor"],
                id_produto=resultado["idProduto"],
                observacoes=resultado["observacoes"],
                preco=resultado["preco"]
            )
    return None

def obter_fornecedores_produto_por_pagina(numero_pagina: int, tamanho_pagina: int) -> List[FornecedorProduto]:
    with obter_conexao() as conexao:
        limite = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor = conexao.execute(OBTER_FORNECEDORES_PRODUTO_POR_PAGINA, (limite, offset))
        resultados = cursor.fetchall()
        return [FornecedorProduto(
            id_fornecedor=r["idFornecedor"],
            id_produto=r["idProduto"],
            observacoes=r["observacoes"],
            preco=r["preco"]
        ) for r in resultados]
