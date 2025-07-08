CRIAR_TABELA_FORNECEDOR_PRODUTO = """
CREATE TABLE IF NOT EXISTS fornecedor_produto (
    id_fornecedor INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    observacoes TEXT,
    preco REAL,
    PRIMARY KEY (id_fornecedor, id_produto),
    FOREIGN KEY (id_fornecedor) REFERENCES usuario(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);
"""

INSERIR_FORNECEDOR_PRODUTO = """
INSERT INTO fornecedor_produto (id_fornecedor, id_produto, observacoes, preco)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_FORNECEDOR_PRODUTO = """
UPDATE fornecedor_produto
SET observacoes = ?, preco = ?
WHERE id_fornecedor = ? AND id_produto = ?;
"""

EXCLUIR_FORNECEDOR_PRODUTO = """
DELETE FROM fornecedor_produto
WHERE id_fornecedor = ? AND id_produto = ?;
"""

OBTER_FORNECEDOR_PRODUTO_POR_ID = """
SELECT id_fornecedor, id_produto, observacoes, preco
FROM fornecedor_produto
WHERE id_fornecedor = ? AND id_produto = ?;
"""

OBTER_FORNECEDORES_PRODUTO_POR_PAGINA = """
SELECT id_fornecedor, id_produto, observacoes, preco
FROM fornecedor_produto
ORDER BY id_fornecedor ASC
LIMIT ? OFFSET ?;
"""
