CRIAR_TABELA_FORNECEDOR = """
CREATE TABLE IF NOT EXISTS fornecedor (
    id INTEGER PRIMARY KEY,
    nome_empresa TEXT,
    cnpj TEXT,
    descricao TEXT,
    prestador BOOLEAN DEFAULT 0,
    vendedor BOOLEAN DEFAULT 0,
    locador BOOLEAN DEFAULT 0,
    verificado BOOLEAN DEFAULT 0,
    data_verificacao DATETIME,
    newsletter BOOLEAN DEFAULT 0,
    FOREIGN KEY (id) REFERENCES usuario(id)
);
"""

INSERIR_FORNECEDOR = """
INSERT INTO fornecedor (id, nome_empresa, cnpj, descricao, prestador, vendedor, locador, verificado, data_verificacao, newsletter)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_FORNECEDOR = """
UPDATE fornecedor
SET nome_empresa = ?, cnpj = ?, descricao = ?, prestador = ?, vendedor = ?, locador = ?, verificado = ?, data_verificacao = ?, newsletter = ?
WHERE id = ?;
"""

EXCLUIR_FORNECEDOR = """
DELETE FROM fornecedor
WHERE id = ?;
"""

OBTER_FORNECEDOR_POR_ID = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao, f.prestador, f.vendedor, f.locador,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
WHERE u.id = ?;
"""

OBTER_FORNECEDORES_POR_PAGINA = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao, f.prestador, f.vendedor, f.locador,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""

OBTER_FORNECEDORES_POR_TIPO = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao, f.prestador, f.vendedor, f.locador,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
WHERE (f.prestador = ? OR f.vendedor = ? OR f.locador = ?)
ORDER BY u.nome ASC;
"""

OBTER_PRESTADORES = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao, f.prestador, f.vendedor, f.locador,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
WHERE f.prestador = 1
ORDER BY u.nome ASC;
"""

OBTER_VENDEDORES = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao, f.prestador, f.vendedor, f.locador,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
WHERE f.vendedor = 1
ORDER BY u.nome ASC;
"""

OBTER_LOCADORES = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.foto, u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao, f.prestador, f.vendedor, f.locador,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
WHERE f.locador = 1
ORDER BY u.nome ASC;
"""
CONTAR_FORNECEDORES = """
SELECT COUNT(*) as total
FROM fornecedor;
"""

CONTAR_FORNECEDORES_NAO_VERIFICADOS = """
SELECT COUNT(*) as total
FROM fornecedor
WHERE verificado = 0;
"""

REJEITAR_FORNECEDOR = """
UPDATE fornecedor
SET verificado = 0, data_verificacao = NULL
WHERE id = ?;
"""
