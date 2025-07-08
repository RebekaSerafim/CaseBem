CRIAR_TABELA_SERVICO = """
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL UNIQUE,

"""

INSERIR_SERVICO = """
INSERT INTO servico (nome, preco, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR_SERVICO= """
UPDATE servico
SET nome = ?, preco = ?, descricao = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_SERVICO = """
UPDATE servico
SET tipo = ?
WHERE id = ?;
"""



EXCLUIR_SERVICO = """
DELETE FROM servico
WHERE id = ?;
"""

OBTER_SERVICO_POR_ID = """
SELECT id, nome, preco, descricao
FROM Usuario
WHERE id = ?;
"""




OBTER_SERVICOS_POR_PAGINA = """
SELECT id, nome, preco, descricao
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""