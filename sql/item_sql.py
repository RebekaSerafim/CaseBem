CRIAR_TABELA_ITEM = """
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fornecedor INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('PRODUTO', 'SERVICO', 'ESPACO')),
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    observacoes TEXT,
    ativo BOOLEAN DEFAULT 1,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id) ON DELETE CASCADE
);
"""

INSERIR_ITEM = """
INSERT INTO item (id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM = """
UPDATE item
SET tipo = ?, nome = ?, descricao = ?, preco = ?, observacoes = ?, ativo = ?
WHERE id = ? AND id_fornecedor = ?;
"""

EXCLUIR_ITEM = """
DELETE FROM item
WHERE id = ? AND id_fornecedor = ?;
"""

OBTER_ITEM_POR_ID = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE id = ?;
"""

OBTER_ITENS_POR_FORNECEDOR = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE id_fornecedor = ? AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_ITENS_POR_TIPO = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE tipo = ? AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_ITENS_POR_PAGINA = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE ativo = 1
ORDER BY data_cadastro DESC
LIMIT ? OFFSET ?;
"""

BUSCAR_ITENS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE ativo = 1 AND (
    nome LIKE ? OR
    descricao LIKE ? OR
    observacoes LIKE ?
)
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_PRODUTOS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE tipo = 'PRODUTO' AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_SERVICOS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE tipo = 'SERVICO' AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_ESPACOS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro
FROM item
WHERE tipo = 'ESPACO' AND ativo = 1
ORDER BY nome ASC;
"""

CONTAR_ITENS_POR_FORNECEDOR = """
SELECT COUNT(*) as total
FROM item
WHERE id_fornecedor = ? AND ativo = 1;
"""

OBTER_ESTATISTICAS_ITENS = """
SELECT
    tipo,
    COUNT(*) as quantidade,
    AVG(preco) as preco_medio,
    MIN(preco) as preco_minimo,
    MAX(preco) as preco_maximo
FROM item
WHERE ativo = 1
GROUP BY tipo;
"""
CONTAR_ITENS = """
SELECT COUNT(*) as total
FROM item;
"""

CONTAR_ITENS_POR_TIPO = """
SELECT COUNT(*) as total
FROM item
WHERE tipo = ?;
"""
