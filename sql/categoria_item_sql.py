CRIAR_TABELA_CATEGORIA_ITEM = """
CREATE TABLE IF NOT EXISTS categoria_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo_fornecimento TEXT NOT NULL,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT 1
);
"""

INSERIR_CATEGORIA_ITEM = """
INSERT INTO categoria_item (nome, tipo_fornecimento, descricao, ativo)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_CATEGORIA_ITEM = """
UPDATE categoria_item
SET nome = ?, tipo_fornecimento = ?, descricao = ?, ativo = ?
WHERE id = ?;
"""

EXCLUIR_CATEGORIA_ITEM = """
DELETE FROM categoria_item
WHERE id = ?;
"""

OBTER_CATEGORIA_ITEM_POR_ID = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria_item
WHERE id = ?;
"""

OBTER_CATEGORIAS_POR_TIPO = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria_item
WHERE tipo_fornecimento = ?
ORDER BY nome ASC;
"""

OBTER_TODAS_CATEGORIAS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria_item
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

OBTER_CATEGORIAS_ATIVAS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria_item
WHERE ativo = 1
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

OBTER_CATEGORIAS_POR_TIPO_ATIVAS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria_item
WHERE tipo_fornecimento = ? AND ativo = 1
ORDER BY nome ASC;
"""