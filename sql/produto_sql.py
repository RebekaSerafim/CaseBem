CRIAR_TABELA_PRODUTO = """
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT NOT NULL
);
"""

INSERIR_PRODUTO = """
INSERT INTO produto (nome, preco, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR_PRODUTO = """
UPDATE produto
SET nome = ?, preco = ?, descricao = ?
WHERE id = ?;
"""

EXCLUIR_PRODUTO = """
DELETE FROM produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_ID = """
SELECT id, nome, preco, descricao
FROM produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_NOME = """
SELECT id, nome, preco, descricao
FROM produto
WHERE nome = ?;
"""

OBTER_PRODUTOS_POR_PAGINA = """
SELECT id, nome, preco, descricao
FROM produto
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""