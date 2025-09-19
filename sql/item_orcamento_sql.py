CRIAR_TABELA_ITEM_ORCAMENTO = """
CREATE TABLE IF NOT EXISTS item_orcamento (
    id_orcamento INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_unitario REAL NOT NULL,
    observacoes TEXT,
    desconto REAL DEFAULT 0,
    PRIMARY KEY (id_orcamento, id_item)
);
"""

INSERIR_ITEM_ORCAMENTO = """
INSERT INTO item_orcamento (id_orcamento, id_item, quantidade, preco_unitario, observacoes, desconto)
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM_ORCAMENTO = """
UPDATE item_orcamento
SET quantidade = ?, preco_unitario = ?, observacoes = ?, desconto = ?
WHERE id_orcamento = ? AND id_item = ?;
"""

EXCLUIR_ITEM_ORCAMENTO = """
DELETE FROM item_orcamento
WHERE id_orcamento = ? AND id_item = ?;
"""

OBTER_ITEM_ORCAMENTO = """
SELECT id_orcamento, id_item, quantidade, preco_unitario, observacoes, desconto
FROM item_orcamento
WHERE id_orcamento = ? AND id_item = ?;
"""

OBTER_ITENS_POR_ORCAMENTO = """
SELECT io.id_orcamento, io.id_item, io.quantidade, io.preco_unitario, io.observacoes, io.desconto,
       i.nome, i.descricao, i.preco, i.tipo,
       (io.quantidade * io.preco_unitario - COALESCE(io.desconto, 0)) as preco_total
FROM item_orcamento io
JOIN item i ON io.id_item = i.id
WHERE io.id_orcamento = ?;
"""

OBTER_TOTAL_ORCAMENTO = """
SELECT SUM(quantidade * preco_unitario - COALESCE(desconto, 0)) as total
FROM item_orcamento
WHERE id_orcamento = ?;
"""

EXCLUIR_ITENS_POR_ORCAMENTO = """
DELETE FROM item_orcamento
WHERE id_orcamento = ?;
"""