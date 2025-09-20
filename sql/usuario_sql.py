CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT,
    data_nascimento TEXT,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'NOIVO',
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN NOT NULL DEFAULT 1
);
"""

INSERIR_USUARIO = """
INSERT INTO Usuario (nome, cpf, data_nascimento, email, telefone, senha, perfil)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_USUARIO = """
UPDATE Usuario
SET nome = ?, cpf = ?, data_nascimento = ?, telefone = ?, email = ?
WHERE id = ?;
"""

ATUALIZAR_SENHA_USUARIO = """
UPDATE Usuario
SET senha = ?
WHERE id = ?;
"""

EXCLUIR_USUARIO = """
DELETE FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_ID = """
SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil, foto, token_redefinicao, data_token, data_cadastro, ativo
FROM Usuario
WHERE id = ?;
"""

OBTER_USUARIO_POR_EMAIL = """
SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil, foto, token_redefinicao, data_token, data_cadastro, ativo
FROM Usuario
WHERE email = ?;
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil, foto, token_redefinicao, data_token, data_cadastro, ativo
FROM Usuario
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_USUARIOS_POR_TIPO_POR_PAGINA = """
SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil, foto, token_redefinicao, data_token, data_cadastro, ativo
FROM Usuario
WHERE perfil = ?
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

CONTAR_USUARIOS = """
SELECT COUNT(*) as total
FROM Usuario;
"""

CONTAR_USUARIOS_POR_TIPO = """
SELECT COUNT(*) as total
FROM Usuario
WHERE perfil = ?;
"""

ADICIONAR_COLUNA_ATIVO = """
ALTER TABLE Usuario ADD COLUMN ativo BOOLEAN NOT NULL DEFAULT 1;
"""

BUSCAR_USUARIOS = """
SELECT id, nome, cpf, data_nascimento, email, telefone, senha, perfil, foto, token_redefinicao, data_token, data_cadastro, ativo
FROM Usuario
WHERE (? = '' OR nome LIKE '%' || ? || '%' OR email LIKE '%' || ? || '%')
  AND (? = '' OR perfil = ?)
  AND (? = '' OR (? = 'ativo' AND ativo = 1) OR (? = 'inativo' AND ativo = 0))
ORDER BY nome ASC
LIMIT ? OFFSET ?;
"""

BLOQUEAR_USUARIO = """
UPDATE Usuario
SET ativo = 0
WHERE id = ?;
"""

ATIVAR_USUARIO = """
UPDATE Usuario
SET ativo = 1
WHERE id = ?;
"""