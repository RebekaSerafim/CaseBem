CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    tipo INTEGER NOT NULL DEFAULT 0);
"""

INSERIR_USUARIO = """
INSERT INTO Usuario (nome, telefone, email, senha_hash, tipo)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE Usuario
SET nome = ?, telefone = ?, email = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_USUARIO = """
UPDATE Usuario
SET tipo = ?
WHERE id = ?;
"""

ATUALIZAR_SENHA_USUARIO = """
UPDATE Usuario
SET senha_hash = ?
WHERE id = ?;
"""

EXCLUIR_USUARIO = """
DELETE FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT id, nome, telefone, email, senha_hash, tipo
FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT id, nome, telefone, email, senha_hash, tipo
FROM Usuario
WHERE email = ?;
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id, nome, telefone, email, senha_hash, tipo
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""