# ==============================================================================
# QUERIES GENÉRICAS (usadas pelo BaseRepo)
# ==============================================================================

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo_fornecimento TEXT NOT NULL,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT 1
);
"""

INSERIR = """
INSERT INTO categoria (nome, tipo_fornecimento, descricao, ativo)
VALUES (?, ?, ?, ?);
"""

INSERIR_COM_ID = """
INSERT INTO categoria (id, nome, tipo_fornecimento, descricao, ativo)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE categoria
SET nome = ?, tipo_fornecimento = ?, descricao = ?, ativo = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM categoria
WHERE id = ?;
"""

OBTER_POR_ID = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE id = ?;
"""

LISTAR_TODOS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

LISTAR_ATIVOS = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE ativo = 1
ORDER BY tipo_fornecimento ASC, nome ASC;
"""

# ==============================================================================
# QUERIES ESPECÍFICAS DE NEGÓCIO (métodos customizados do repositório)
# ==============================================================================

OBTER_CATEGORIAS_POR_TIPO = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE tipo_fornecimento = ?
ORDER BY nome ASC;
"""

OBTER_CATEGORIAS_ATIVAS_POR_TIPO = """
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

CONTAR_CATEGORIAS_FILTRADAS = """
SELECT COUNT(*) as total
FROM categoria
WHERE (? = '' OR nome LIKE ? OR descricao LIKE ?)
  AND (? = '' OR tipo_fornecimento = ?)
  AND (? = '' OR (? = 'ativo' AND ativo = 1) OR (? = 'inativo' AND ativo = 0));
"""

BUSCAR_CATEGORIAS_PAGINADO = """
SELECT id, nome, tipo_fornecimento, descricao, ativo
FROM categoria
WHERE (? = '' OR nome LIKE ? OR descricao LIKE ?)
  AND (? = '' OR tipo_fornecimento = ?)
  AND (? = '' OR (? = 'ativo' AND ativo = 1) OR (? = 'inativo' AND ativo = 0))
ORDER BY tipo_fornecimento ASC, nome ASC
LIMIT ? OFFSET ?;
"""

# Queries ATIVAR_CATEGORIA e DESATIVAR_CATEGORIA removidas:
# Use BaseRepo.ativar(id) e BaseRepo.desativar(id) ao invés
