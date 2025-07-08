CRIAR_TABELA_ITEM_DEMANDA_PRODUTO = """
CREATE TABLE IF NOT EXISTS item_demanda_produto (
    id_demanda INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_demanda, id_produto),
    FOREIGN KEY (id_demanda) REFERENCES demanda(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);
"""

INSERIR_ITEM_DEMANDA_PRODUTO = """
INSERT INTO item_demanda_produto (id_demanda, id_produto, quantidade, observacoes)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_ITEM_DEMANDA_PRODUTO = """
UPDATE item_demanda_produto
SET quantidade = ?, observacoes = ?
WHERE id_demanda = ? AND id_produto = ?;
"""

EXCLUIR_ITEM_DEMANDA_PRODUTO = """
DELETE FROM item_demanda_produto
WHERE id_demanda = ? AND id_produto = ?;
"""

OBTER_ITEM_DEMANDA_PRODUTO_POR_ID = """
SELECT id_demanda, id_produto, quantidade, observacoes
FROM item_demanda_produto
WHERE id_demanda = ? AND id_produto = ?;
"""

OBTER_ITENS_POR_DEMANDA = """
SELECT id_demanda, id_produto, quantidade, observacoes
FROM item_demanda_produto
WHERE id_demanda = ?
ORDER BY id_produto ASC;
"""

OBTER_ITENS_DEMANDA_PRODUTO_POR_PAGINA = """
SELECT id_demanda, id_produto, quantidade, observacoes
FROM item_demanda_produto
ORDER BY id_demanda ASC, id_produto ASC
LIMIT ? OFFSET ?;
"""