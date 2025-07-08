CRIAR_TABELA_ITEM_ORCAMENTO_SERVICO = """
CREATE TABLE IF NOT EXISTS item_orcamento_servico (
    id_orcamento INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_orcamento, id_servico),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id) ON DELETE CASCADE
);
"""

INSERIR_ITEM_ORCAMENTO_SERVICO = """
INSERT INTO item_orcamento_servico (id_orcamento, id_servico, preco_unitario, quantidade, observacoes)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM_ORCAMENTO_SERVICO = """
UPDATE item_orcamento_servico
SET preco_unitario = ?, quantidade = ?, observacoes = ?
WHERE id_orcamento = ? AND id_servico = ?;
"""

EXCLUIR_ITEM_ORCAMENTO_SERVICO = """
DELETE FROM item_orcamento_servico
WHERE id_orcamento = ? AND id_servico = ?;
"""

OBTER_ITEM_ORCAMENTO_SERVICO_POR_ID = """
SELECT id_orcamento, id_servico, preco_unitario, quantidade, observacoes
FROM item_orcamento_servico
WHERE id_orcamento = ? AND id_servico = ?;
"""

OBTER_ITENS_POR_ORCAMENTO = """
SELECT id_orcamento, id_servico, preco_unitario, quantidade, observacoes
FROM item_orcamento_servico
WHERE id_orcamento = ?
ORDER BY id_servico;
"""

OBTER_ITENS_ORCAMENTO_SERVICO_POR_PAGINA = """
SELECT id_orcamento, id_servico, preco_unitario, quantidade, observacoes
FROM item_orcamento_servico
ORDER BY id_orcamento, id_servico
LIMIT ? OFFSET ?;
"""

CALCULAR_TOTAL_ITENS_SERVICO_ORCAMENTO = """
SELECT SUM(preco_unitario * quantidade) as total
FROM item_orcamento_servico
WHERE id_orcamento = ?;
"""