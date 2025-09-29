CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo_fornecimento TEXT NOT NULL,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT 1
);
"""

CRIAR_TABELA_CATEGORIA = CRIAR_TABELA

INSERIR = """
INSERT INTO categoria (nome, tipo_fornecimento, descricao, ativo)
VALUES (?, ?, ?, ?);
"""

INSERIR_CATEGORIA = INSERIR

ATUALIZAR = """
UPDATE categoria
SET nome = ?, tipo_fornecimento = ?, descricao = ?, ativo = ?
WHERE id = ?;
"""

ATUALIZAR_CATEGORIA = ATUALIZAR

EXCLUIR = """
DELETE FROM categoria
WHERE id = ?;
"""

EXCLUIR_CATEGORIA = EXCLUIR

OBTER_POR_ID = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE id = ?;
"""

OBTER_CATEGORIA_POR_ID = OBTER_POR_ID

OBTER_CATEGORIAS_POR_TIPO = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE tipo_fornecimento = ?
ORDER BY nome ASC;
"""

LISTAR_TODOS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

OBTER_TODAS_CATEGORIAS = LISTAR_TODOS

LISTAR_ATIVOS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE ativo = 1
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

OBTER_CATEGORIAS_ATIVAS = LISTAR_ATIVOS

OBTER_CATEGORIAS_POR_TIPO_ATIVAS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE tipo_fornecimento = ? AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_CATEGORIA_POR_NOME = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE nome = ? AND tipo_fornecimento = ?;
"""

BUSCAR_CATEGORIAS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE (? = '' OR nome LIKE ? OR descricao LIKE ?)
  AND (? = '' OR tipo_fornecimento = ?)
  AND (? = '' OR (? = 'ativo' AND ativo = 1) OR (? = 'inativo' AND ativo = 0))
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

ATIVAR_CATEGORIA = """
UPDATE categoria
SET ativo = 1
WHERE id = ?;
"""

DESATIVAR_CATEGORIA = """
UPDATE categoria
SET ativo = 0
WHERE id = ?;
"""