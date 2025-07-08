CRIAR_TABELA_ITEM_DEMANDA_SERVICO = """
CREATE TABLE IF NOT EXISTS item_demanda_servico (
    id_demanda INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    PRIMARY KEY (id_demanda, id_servico),
    FOREIGN KEY (id_demanda) REFERENCES demanda(id),
    FOREIGN KEY (id_servico) REFERENCES servico(id)
);
"""

INSERIR_ITEM_DEMANDA_SERVICO = """
INSERT INTO item_demanda_servico (id_demanda, id_servico, quantidade, observacoes)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_ITEM_DEMANDA_SERVICO = """
UPDATE item_demanda_servico
SET quantidade = ?, observacoes = ?
WHERE id_demanda = ? AND id_servico = ?;
"""

EXCLUIR_ITEM_DEMANDA_SERVICO = """
DELETE FROM item_demanda_servico
WHERE id_demanda = ? AND id_servico = ?;
"""

OBTER_ITEM_DEMANDA_SERVICO_POR_ID = """
SELECT id_demanda, id_servico, quantidade, observacoes
FROM item_demanda_servico
WHERE id_demanda = ? AND id_servico = ?;
"""

OBTER_ITENS_POR_DEMANDA = """
SELECT id_demanda, id_servico, quantidade, observacoes
FROM item_demanda_servico
WHERE id_demanda = ?
ORDER BY id_servico ASC;
"""

OBTER_ITENS_DEMANDA_SERVICO_POR_PAGINA = """
SELECT id_demanda, id_servico, quantidade, observacoes
FROM item_demanda_servico
ORDER BY id_demanda ASC, id_servico ASC
LIMIT ? OFFSET ?;
"""