CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'cliente',
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERIR_USUARIO = """
INSERT INTO Usuario (nome, telefone, email, senha_hash, tipo, documento)
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE Usuario
SET nome = ?, telefone = ?, email = ?, documento = ?
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
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
WHERE email = ?;
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_USUARIOS_POR_TIPO_POR_PAGINA = """
SELECT id, nome, telefone, email, senha_hash, tipo, documento
FROM Usuario
WHERE tipo = ?
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""