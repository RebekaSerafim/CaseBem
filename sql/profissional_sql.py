CRIAR_TABELA_PROFISSIONAL = """
CREATE TABLE IF NOT EXISTS profissional (
    id INTEGER PRIMARY KEY,
    nome_empresa TEXT,
    cnpj TEXT,
    descricao TEXT,
    prestador BOOLEAN DEFAULT 0,
    fornecedor BOOLEAN DEFAULT 0,
    locador BOOLEAN DEFAULT 0,
    FOREIGN KEY (id) REFERENCES usuario(id)
);
"""

INSERIR_PROFISSIONAL = """
INSERT INTO profissional (id, nome_empresa, cnpj, descricao, prestador, fornecedor, locador)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_PROFISSIONAL = """
UPDATE profissional
SET nome_empresa = ?, cnpj = ?, descricao = ?, prestador = ?, fornecedor = ?, locador = ?
WHERE id = ?;
"""

EXCLUIR_PROFISSIONAL = """
DELETE FROM profissional
WHERE id = ?;
"""

OBTER_PROFISSIONAL_POR_ID = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       p.nome_empresa, p.cnpj, p.descricao, p.prestador, p.fornecedor, p.locador
FROM usuario u
JOIN profissional p ON u.id = p.id
WHERE u.id = ?;
"""

OBTER_PROFISSIONAIS_POR_PAGINA = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       p.nome_empresa, p.cnpj, p.descricao, p.prestador, p.fornecedor, p.locador
FROM usuario u
JOIN profissional p ON u.id = p.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_PROFISSIONAIS_POR_TIPO = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       p.nome_empresa, p.cnpj, p.descricao, p.prestador, p.fornecedor, p.locador
FROM usuario u
JOIN profissional p ON u.id = p.id
WHERE (p.prestador = ? OR p.fornecedor = ? OR p.locador = ?)
ORDER BY u.nome ASC;
"""

OBTER_PRESTADORES = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       p.nome_empresa, p.cnpj, p.descricao, p.prestador, p.fornecedor, p.locador
FROM usuario u
JOIN profissional p ON u.id = p.id
WHERE p.prestador = 1
ORDER BY u.nome ASC;
"""

OBTER_FORNECEDORES = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       p.nome_empresa, p.cnpj, p.descricao, p.prestador, p.fornecedor, p.locador
FROM usuario u
JOIN profissional p ON u.id = p.id
WHERE p.fornecedor = 1
ORDER BY u.nome ASC;
"""

OBTER_LOCADORES = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       p.nome_empresa, p.cnpj, p.descricao, p.prestador, p.fornecedor, p.locador
FROM usuario u
JOIN profissional p ON u.id = p.id
WHERE p.locador = 1
ORDER BY u.nome ASC;
"""