"""
Queries SQL para o domínio de Usuários

Centraliza todas as queries relacionadas a usuários, fornecedores
e operações de autenticação.
"""

from .base_queries import gerar_create_table, gerar_insert, gerar_update, gerar_select_por_id

# Definição da estrutura da tabela usuario
USUARIO_COLUNAS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "nome": "TEXT NOT NULL",
    "cpf": "TEXT",
    "data_nascimento": "TEXT",
    "email": "TEXT UNIQUE NOT NULL",
    "telefone": "TEXT NOT NULL",
    "senha": "TEXT NOT NULL",
    "perfil": "TEXT NOT NULL",
    "token_redefinicao": "TEXT",
    "data_token": "TEXT",
    "data_cadastro": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "ativo": "INTEGER DEFAULT 1"
}

# Queries básicas da tabela usuario
CRIAR_TABELA_USUARIO = gerar_create_table("usuario", USUARIO_COLUNAS)

INSERIR_USUARIO = gerar_insert("usuario", [
    "nome", "cpf", "data_nascimento", "email", "telefone", "senha", "perfil"
])

ATUALIZAR_USUARIO = gerar_update("usuario", [
    "nome", "cpf", "data_nascimento", "telefone", "email"
])

OBTER_USUARIO_POR_ID = gerar_select_por_id("usuario")

# Queries específicas do domínio
OBTER_USUARIO_POR_EMAIL = """
SELECT * FROM usuario
WHERE email = ? AND ativo = 1
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT * FROM usuario
ORDER BY data_cadastro DESC
LIMIT ? OFFSET ?
"""

OBTER_USUARIOS_POR_PERFIL = """
SELECT * FROM usuario
WHERE perfil = ? AND ativo = 1
ORDER BY nome
"""

CONTAR_USUARIOS = """
SELECT COUNT(*) FROM usuario
WHERE ativo = 1
"""

CONTAR_USUARIOS_POR_PERFIL = """
SELECT COUNT(*) FROM usuario
WHERE perfil = ? AND ativo = 1
"""

ATUALIZAR_SENHA_USUARIO = """
UPDATE usuario
SET senha = ?
WHERE id = ?
"""

ATUALIZAR_TOKEN_REDEFINICAO = """
UPDATE usuario
SET token_redefinicao = ?, data_token = ?
WHERE id = ?
"""

LIMPAR_TOKEN_REDEFINICAO = """
UPDATE usuario
SET token_redefinicao = NULL, data_token = NULL
WHERE id = ?
"""

OBTER_USUARIO_POR_TOKEN = """
SELECT * FROM usuario
WHERE token_redefinicao = ? AND ativo = 1
"""

DESATIVAR_USUARIO = """
UPDATE usuario
SET ativo = 0
WHERE id = ?
"""

ATIVAR_USUARIO = """
UPDATE usuario
SET ativo = 1
WHERE id = ?
"""

# Queries para fornecedores (extensão de usuários)
FORNECEDOR_COLUNAS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "nome": "TEXT NOT NULL",
    "cpf": "TEXT",
    "data_nascimento": "TEXT",
    "email": "TEXT UNIQUE NOT NULL",
    "telefone": "TEXT NOT NULL",
    "senha": "TEXT NOT NULL",
    "perfil": "TEXT NOT NULL DEFAULT 'FORNECEDOR'",
    "token_redefinicao": "TEXT",
    "data_token": "TEXT",
    "data_cadastro": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "ativo": "INTEGER DEFAULT 1",
    "nome_empresa": "TEXT",
    "cnpj": "TEXT",
    "descricao": "TEXT",
    "verificado": "INTEGER DEFAULT 0",
    "data_verificacao": "TEXT",
    "newsletter": "INTEGER DEFAULT 0"
}

CRIAR_TABELA_FORNECEDOR = gerar_create_table("fornecedor", FORNECEDOR_COLUNAS)

INSERIR_FORNECEDOR = gerar_insert("fornecedor", [
    "nome", "cpf", "data_nascimento", "email", "telefone", "senha", "perfil",
    "nome_empresa", "cnpj", "descricao", "newsletter"
])

ATUALIZAR_FORNECEDOR = gerar_update("fornecedor", [
    "nome", "cpf", "data_nascimento", "telefone", "email",
    "nome_empresa", "cnpj", "descricao", "newsletter"
])

OBTER_FORNECEDOR_POR_ID = gerar_select_por_id("fornecedor")

OBTER_FORNECEDOR_POR_EMAIL = """
SELECT * FROM fornecedor
WHERE email = ? AND ativo = 1
"""

OBTER_FORNECEDORES_VERIFICADOS = """
SELECT * FROM fornecedor
WHERE verificado = 1 AND ativo = 1
ORDER BY nome_empresa
"""

OBTER_FORNECEDORES_PENDENTES = """
SELECT * FROM fornecedor
WHERE verificado = 0 AND ativo = 1
ORDER BY data_cadastro
"""

VERIFICAR_FORNECEDOR = """
UPDATE fornecedor
SET verificado = 1, data_verificacao = ?
WHERE id = ?
"""

OBTER_FORNECEDORES_POR_PAGINA = """
SELECT * FROM fornecedor
WHERE ativo = 1
ORDER BY nome_empresa
LIMIT ? OFFSET ?
"""

CONTAR_FORNECEDORES_ATIVOS = """
SELECT COUNT(*) FROM fornecedor
WHERE ativo = 1
"""

CONTAR_FORNECEDORES_VERIFICADOS = """
SELECT COUNT(*) FROM fornecedor
WHERE verificado = 1 AND ativo = 1
"""

# Query para buscar fornecedores por termo
BUSCAR_FORNECEDORES = """
SELECT * FROM fornecedor
WHERE ativo = 1
AND (
    nome_empresa LIKE ? OR
    nome LIKE ? OR
    descricao LIKE ?
)
ORDER BY
    CASE WHEN verificado = 1 THEN 0 ELSE 1 END,
    nome_empresa
"""

# Adicionar coluna ativo para compatibilidade com versões antigas
ADICIONAR_COLUNA_ATIVO = """
ALTER TABLE usuario ADD COLUMN ativo INTEGER DEFAULT 1
"""

# Query para estatísticas de usuários
ESTATISTICAS_USUARIOS = """
SELECT
    perfil,
    COUNT(*) as total,
    COUNT(CASE WHEN ativo = 1 THEN 1 END) as ativos
FROM usuario
GROUP BY perfil
"""