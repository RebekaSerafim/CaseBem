"""
Queries SQL para o domínio de Categorias e Itens

Centraliza todas as queries relacionadas a categorias, itens,
e suas relações com fornecedores.
"""

from .base_queries import gerar_create_table, gerar_insert, gerar_update, gerar_select_por_id

# Definição da estrutura da tabela categoria
CATEGORIA_COLUNAS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "nome": "TEXT NOT NULL",
    "tipo_fornecimento": "TEXT NOT NULL",
    "descricao": "TEXT",
    "ativo": "INTEGER DEFAULT 1"
}

# Queries básicas da tabela categoria
CRIAR_TABELA_CATEGORIA = gerar_create_table("categoria", CATEGORIA_COLUNAS)

INSERIR_CATEGORIA = gerar_insert("categoria", [
    "nome", "tipo_fornecimento", "descricao"
])

ATUALIZAR_CATEGORIA = gerar_update("categoria", [
    "nome", "tipo_fornecimento", "descricao"
])

OBTER_CATEGORIA_POR_ID = gerar_select_por_id("categoria")

# Queries específicas de categoria
OBTER_TODAS_CATEGORIAS = """
SELECT * FROM categoria
ORDER BY nome
"""

OBTER_CATEGORIAS_ATIVAS = """
SELECT * FROM categoria
WHERE ativo = 1
ORDER BY nome
"""

OBTER_CATEGORIAS_POR_TIPO = """
SELECT * FROM categoria
WHERE tipo_fornecimento = ?
ORDER BY nome
"""

OBTER_CATEGORIAS_POR_TIPO_ATIVAS = """
SELECT * FROM categoria
WHERE tipo_fornecimento = ? AND ativo = 1
ORDER BY nome
"""

OBTER_CATEGORIA_POR_NOME = """
SELECT * FROM categoria
WHERE nome = ?
"""

OBTER_CATEGORIA_POR_NOME_E_TIPO = """
SELECT * FROM categoria
WHERE nome = ? AND tipo_fornecimento = ?
"""

BUSCAR_CATEGORIAS_POR_NOME = """
SELECT * FROM categoria
WHERE nome LIKE ? AND ativo = 1
ORDER BY nome
"""

CONTAR_CATEGORIAS_ATIVAS = """
SELECT COUNT(*) FROM categoria
WHERE ativo = 1
"""

CONTAR_CATEGORIAS_POR_TIPO = """
SELECT COUNT(*) FROM categoria
WHERE tipo_fornecimento = ? AND ativo = 1
"""

# Definição da estrutura da tabela item
ITEM_COLUNAS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "id_fornecedor": "INTEGER NOT NULL",
    "tipo": "TEXT NOT NULL",
    "nome": "TEXT NOT NULL",
    "descricao": "TEXT",
    "preco": "REAL NOT NULL",
    "id_categoria": "INTEGER NOT NULL",
    "observacoes": "TEXT",
    "ativo": "INTEGER DEFAULT 1",
    "data_cadastro": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
}

# Queries básicas da tabela item
CRIAR_TABELA_ITEM = gerar_create_table("item", ITEM_COLUNAS)

INSERIR_ITEM = gerar_insert("item", [
    "id_fornecedor", "tipo", "nome", "descricao", "preco", "id_categoria", "observacoes"
])

ATUALIZAR_ITEM = gerar_update("item", [
    "nome", "descricao", "preco", "id_categoria", "observacoes"
])

OBTER_ITEM_POR_ID = gerar_select_por_id("item")

# Queries específicas de item
OBTER_ITENS_ATIVOS = """
SELECT * FROM item
WHERE ativo = 1
ORDER BY nome
"""

OBTER_ITENS_POR_CATEGORIA = """
SELECT * FROM item
WHERE id_categoria = ? AND ativo = 1
ORDER BY nome
"""

OBTER_ITENS_POR_FORNECEDOR = """
SELECT * FROM item
WHERE id_fornecedor = ? AND ativo = 1
ORDER BY nome
"""

OBTER_ITENS_POR_TIPO = """
SELECT * FROM item
WHERE tipo = ? AND ativo = 1
ORDER BY nome
"""

OBTER_ITENS_POR_FAIXA_PRECO = """
SELECT * FROM item
WHERE preco BETWEEN ? AND ? AND ativo = 1
ORDER BY preco
"""

BUSCAR_ITENS = """
SELECT i.*, c.nome as categoria_nome, f.nome_empresa
FROM item i
LEFT JOIN categoria c ON i.id_categoria = c.id
LEFT JOIN fornecedor f ON i.id_fornecedor = f.id
WHERE i.ativo = 1
AND (
    i.nome LIKE ? OR
    i.descricao LIKE ? OR
    c.nome LIKE ?
)
ORDER BY i.nome
"""

BUSCAR_ITENS_COM_FILTROS = """
SELECT i.*, c.nome as categoria_nome, f.nome_empresa
FROM item i
LEFT JOIN categoria c ON i.id_categoria = c.id
LEFT JOIN fornecedor f ON i.id_fornecedor = f.id
WHERE i.ativo = 1
AND (? IS NULL OR i.id_categoria = ?)
AND (? IS NULL OR i.tipo = ?)
AND (? IS NULL OR i.preco <= ?)
AND (? IS NULL OR (i.nome LIKE ? OR i.descricao LIKE ?))
ORDER BY i.preco, i.nome
"""

OBTER_ITENS_POPULARES = """
SELECT i.*, COUNT(oi.id_item) as uso_count
FROM item i
LEFT JOIN orcamento_item oi ON i.id = oi.id_item
WHERE i.ativo = 1
GROUP BY i.id
ORDER BY uso_count DESC, i.nome
LIMIT ?
"""

CONTAR_ITENS_POR_CATEGORIA = """
SELECT COUNT(*) FROM item
WHERE id_categoria = ? AND ativo = 1
"""

CONTAR_ITENS_POR_FORNECEDOR = """
SELECT COUNT(*) FROM item
WHERE id_fornecedor = ? AND ativo = 1
"""

OBTER_ESTATISTICAS_ITENS = """
SELECT
    COUNT(*) as total_itens,
    COUNT(CASE WHEN ativo = 1 THEN 1 END) as itens_ativos,
    AVG(preco) as preco_medio,
    MIN(preco) as preco_minimo,
    MAX(preco) as preco_maximo
FROM item
"""

# Queries para relacionamento categoria-fornecedor
OBTER_CATEGORIAS_COM_ITENS = """
SELECT DISTINCT c.*
FROM categoria c
INNER JOIN item i ON c.id = i.id_categoria
WHERE c.ativo = 1 AND i.ativo = 1
ORDER BY c.nome
"""

OBTER_FORNECEDORES_POR_CATEGORIA = """
SELECT DISTINCT f.*
FROM fornecedor f
INNER JOIN item i ON f.id = i.id_fornecedor
WHERE i.id_categoria = ? AND f.ativo = 1 AND i.ativo = 1
ORDER BY f.nome_empresa
"""

# Queries para dashboard/relatórios
RELATORIO_ITENS_POR_CATEGORIA = """
SELECT
    c.nome as categoria,
    c.tipo_fornecimento,
    COUNT(i.id) as total_itens,
    AVG(i.preco) as preco_medio
FROM categoria c
LEFT JOIN item i ON c.id = i.id_categoria AND i.ativo = 1
WHERE c.ativo = 1
GROUP BY c.id, c.nome, c.tipo_fornecimento
ORDER BY total_itens DESC, c.nome
"""

ITENS_MAIS_CAROS_POR_CATEGORIA = """
SELECT
    c.nome as categoria,
    i.nome as item,
    i.preco,
    f.nome_empresa as fornecedor
FROM item i
INNER JOIN categoria c ON i.id_categoria = c.id
INNER JOIN fornecedor f ON i.id_fornecedor = f.id
WHERE i.ativo = 1
AND i.preco = (
    SELECT MAX(i2.preco)
    FROM item i2
    WHERE i2.id_categoria = c.id AND i2.ativo = 1
)
ORDER BY c.nome, i.preco DESC
"""