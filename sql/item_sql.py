CRIAR_TABELA_ITEM = """
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fornecedor INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('PRODUTO', 'SERVIÇO', 'ESPAÇO')),
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    id_categoria INTEGER NOT NULL,
    observacoes TEXT,
    ativo BOOLEAN DEFAULT 1,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);
"""

INSERIR_ITEM = """
INSERT INTO item (id_fornecedor, tipo, nome, descricao, preco, id_categoria, observacoes, ativo)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_ITEM = """
UPDATE item
SET tipo = ?, nome = ?, descricao = ?, preco = ?, id_categoria = ?, observacoes = ?, ativo = ?
WHERE id = ? AND id_fornecedor = ?;
"""

EXCLUIR_ITEM = """
DELETE FROM item
WHERE id = ? AND id_fornecedor = ?;
"""

OBTER_ITEM_POR_ID = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE id = ?;
"""

OBTER_ITENS_POR_FORNECEDOR = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE id_fornecedor = ? AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_ITENS_POR_TIPO = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE tipo = ? AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_ITENS_POR_PAGINA = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
ORDER BY data_cadastro DESC
LIMIT ? OFFSET ?;
"""

BUSCAR_ITENS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE (
    nome LIKE ? OR
    descricao LIKE ? OR
    observacoes LIKE ?
)
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_PRODUTOS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE tipo = 'PRODUTO' AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_SERVICOS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE tipo = 'SERVIÇO' AND ativo = 1
ORDER BY nome ASC;
"""

OBTER_ESPACOS = """
SELECT id, id_fornecedor, tipo, nome, descricao, preco, observacoes, ativo, data_cadastro, id_categoria
FROM item
WHERE tipo = 'ESPAÇO' AND ativo = 1
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

OBTER_ITENS_PUBLICOS_FILTRADOS = """
SELECT i.id, i.id_fornecedor, i.tipo, i.nome, i.descricao, i.preco, i.observacoes, i.ativo, i.data_cadastro, i.id_categoria,
       u.nome as fornecedor_nome, f.nome_empresa as fornecedor_empresa, c.nome as categoria_nome
FROM item i
JOIN usuario u ON i.id_fornecedor = u.id
LEFT JOIN fornecedor f ON i.id_fornecedor = f.id
LEFT JOIN categoria c ON i.id_categoria = c.id
WHERE i.ativo = 1
  AND (? IS NULL OR i.tipo = ?)
  AND (? IS NULL OR i.nome LIKE ? OR i.descricao LIKE ? OR i.observacoes LIKE ?)
  AND (? IS NULL OR i.id_categoria = ?)
ORDER BY i.data_cadastro DESC
LIMIT ? OFFSET ?;
"""

CONTAR_ITENS_PUBLICOS_FILTRADOS = """
SELECT COUNT(*) as total
FROM item i
JOIN usuario u ON i.id_fornecedor = u.id
LEFT JOIN categoria c ON i.id_categoria = c.id
WHERE i.ativo = 1
  AND (? IS NULL OR i.tipo = ?)
  AND (? IS NULL OR i.nome LIKE ? OR i.descricao LIKE ? OR i.observacoes LIKE ?)
  AND (? IS NULL OR i.id_categoria = ?);
"""
