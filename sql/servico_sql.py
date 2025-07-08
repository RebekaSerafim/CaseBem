CRIAR_TABELA_SERVICO = """
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT NOT NULL
);
"""

INSERIR_SERVICO = """
INSERT INTO servico (nome, preco, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR_SERVICO = """
UPDATE servico
SET nome = ?, preco = ?, descricao = ?
WHERE id = ?;
"""

EXCLUIR_SERVICO = """
DELETE FROM servico
WHERE id = ?;
"""

OBTER_SERVICO_POR_ID = """
SELECT id, nome, preco, descricao
FROM servico
WHERE id = ?;
"""

OBTER_SERVICO_POR_NOME = """
SELECT id, nome, preco, descricao
FROM servico
WHERE nome = ?;
"""

OBTER_SERVICOS_POR_PAGINA = """
SELECT id, nome, preco, descricao
FROM servico
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""