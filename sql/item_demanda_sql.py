CRIAR_TABELA_ITEM_DEMANDA = """
CREATE TABLE IF NOT EXISTS item_demanda (
    id_demanda INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    observacoes TEXT,
    preco_maximo REAL,
    PRIMARY KEY (id_demanda, id_item)
);
"""

# Queries compatíveis com BaseRepoChaveComposta
CRIAR_TABELA = CRIAR_TABELA_ITEM_DEMANDA

INSERIR = """
INSERT INTO item_demanda (id_demanda, id_item, quantidade, observacoes, preco_maximo)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE item_demanda
SET quantidade = ?, observacoes = ?, preco_maximo = ?
WHERE id_demanda = ? AND id_item = ?;
"""

EXCLUIR = """
DELETE FROM item_demanda
WHERE id_demanda = ? AND id_item = ?;
"""

OBTER_POR_CHAVE = """
SELECT id_demanda, id_item, quantidade, observacoes, preco_maximo
FROM item_demanda
WHERE id_demanda = ? AND id_item = ?;
"""

LISTAR_TODOS = """
SELECT id_demanda, id_item, quantidade, observacoes, preco_maximo
FROM item_demanda
ORDER BY id_demanda, id_item;
"""

# Queries específicas do domínio (mantidas para compatibilidade)
INSERIR_ITEM_DEMANDA = INSERIR
ATUALIZAR_ITEM_DEMANDA = ATUALIZAR
EXCLUIR_ITEM_DEMANDA = EXCLUIR
OBTER_ITEM_DEMANDA = OBTER_POR_CHAVE

OBTER_ITENS_POR_DEMANDA = """
SELECT id.id_demanda, id.id_item, id.quantidade, id.observacoes, id.preco_maximo,
       i.nome, i.descricao, i.preco, i.tipo
FROM item_demanda id
JOIN item i ON id.id_item = i.id
WHERE id.id_demanda = ?;
"""

EXCLUIR_ITENS_POR_DEMANDA = """
DELETE FROM item_demanda
WHERE id_demanda = ?;
"""