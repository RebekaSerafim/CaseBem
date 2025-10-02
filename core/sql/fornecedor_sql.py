# ==============================================================================
# QUERIES GENÉRICAS (usadas pelo BaseRepo)
# ==============================================================================

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS fornecedor (
    id INTEGER PRIMARY KEY,
    nome_empresa TEXT,
    cnpj TEXT,
    descricao TEXT,
    verificado BOOLEAN DEFAULT 0,
    data_verificacao DATETIME,
    newsletter BOOLEAN DEFAULT 0,
    FOREIGN KEY (id) REFERENCES usuario(id)
);
"""

INSERIR = """
INSERT INTO fornecedor (id, nome_empresa, cnpj, descricao, verificado, data_verificacao, newsletter)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE fornecedor
SET nome_empresa = ?, cnpj = ?, descricao = ?, verificado = ?, data_verificacao = ?, newsletter = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM fornecedor
WHERE id = ?;
"""

OBTER_POR_ID = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
WHERE u.id = ?;
"""

LISTAR_TODOS = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
ORDER BY u.nome ASC;
"""

# ==============================================================================
# QUERIES ESPECÍFICAS DE NEGÓCIO (métodos customizados do repositório)
# ==============================================================================

OBTER_FORNECEDORES_POR_PAGINA = """
SELECT u.id, u.nome, u.cpf, u.data_nascimento, u.email, u.telefone, u.senha, u.perfil,
       u.token_redefinicao, u.data_token, u.data_cadastro,
       f.nome_empresa, f.cnpj, f.descricao,
       f.verificado, f.data_verificacao, f.newsletter
FROM usuario u
JOIN fornecedor f ON u.id = f.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""

CONTAR_FORNECEDORES_NAO_VERIFICADOS = """
SELECT COUNT(*) as total
FROM fornecedor
WHERE verificado = 0;
"""

# Query CONTAR_FORNECEDORES removida: Use BaseRepo.contar_registros() ao invés

REJEITAR_FORNECEDOR = """
UPDATE fornecedor
SET verificado = 0, data_verificacao = NULL
WHERE id = ?;
"""

EXCLUIR_USUARIO_FORNECEDOR = "DELETE FROM usuario WHERE id = ?"
