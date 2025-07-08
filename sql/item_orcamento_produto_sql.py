CRIAR_TABELA_ITEM_ORCAMENTO_PRODUTO = """
CREATE TABLE IF NOT EXISTS item_orcamento_produto (
    id_orcamento INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_orcamento, id_produto),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id) ON DELETE CASCADE
);
"""

INSERIR_ITEM_ORCAMENTO_PRODUTO = """
INSERT INTO item_orcamento_produto (id_orcamento, id_produto, preco_unitario, quantidade, observacoes)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM_ORCAMENTO_PRODUTO = """
UPDATE item_orcamento_produto
SET preco_unitario = ?, quantidade = ?, observacoes = ?
WHERE id_orcamento = ? AND id_produto = ?;
"""

EXCLUIR_ITEM_ORCAMENTO_PRODUTO = """
DELETE FROM item_orcamento_produto
WHERE id_orcamento = ? AND id_produto = ?;
"""

OBTER_ITEM_ORCAMENTO_PRODUTO_POR_ID = """
SELECT id_orcamento, id_produto, preco_unitario, quantidade, observacoes
FROM item_orcamento_produto
WHERE id_orcamento = ? AND id_produto = ?;
"""

OBTER_ITENS_POR_ORCAMENTO = """
SELECT id_orcamento, id_produto, preco_unitario, quantidade, observacoes
FROM item_orcamento_produto
WHERE id_orcamento = ?
ORDER BY id_produto;
"""

OBTER_ITENS_ORCAMENTO_PRODUTO_POR_PAGINA = """
SELECT id_orcamento, id_produto, preco_unitario, quantidade, observacoes
FROM item_orcamento_produto
ORDER BY id_orcamento, id_produto
LIMIT ? OFFSET ?;
"""

CALCULAR_TOTAL_ITENS_PRODUTO_ORCAMENTO = """
SELECT SUM(preco_unitario * quantidade) as total
FROM item_orcamento_produto
WHERE id_orcamento = ?;
"""