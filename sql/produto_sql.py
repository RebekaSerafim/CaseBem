CRIAR_TABELA_PRODUTO = """
CREATE TABLE IF NOT EXISTS Produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco FLOAT NOT NULL DEFAULT 0,
    quantidade INTEGER NOT NULL DEFAULT 0,
    descricao TEXT NOT NULL);
"""

INSERIR_PRODUTO = """
INSERT INTO Produto (nome, preco, quantidade, descricao)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_PRODUTO = """
UPDATE Produto
SET nome = ?, preco = ?, quantidade = ?, descricao = ?
WHERE id = ?;
"""

EXCLUIR_PRODUTO = """
DELETE FROM Produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_ID = """
SELECT id, nome, preco, quantidade, descricao
FROM Produto
WHERE id = ?;
"""

OBTER_PRODUTO_POR_NOME = """
SELECT id, nome, preco, quantidade, descricao
FROM Produto
WHERE email = ?;
"""

OBTER_PRODUTOS_POR_PAGINA = """
SELECT id, nome, preco, quantidade, descricao
FROM Produto
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""