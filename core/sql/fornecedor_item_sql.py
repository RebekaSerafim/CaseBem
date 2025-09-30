CRIAR_TABELA_FORNECEDOR_ITEM = """
CREATE TABLE IF NOT EXISTS fornecedor_item (
    id_fornecedor INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    observacoes TEXT,
    preco_personalizado REAL,
    disponivel BOOLEAN NOT NULL DEFAULT 1,
    PRIMARY KEY (id_fornecedor, id_item)
);
"""

# Queries compatíveis com BaseRepoChaveComposta
CRIAR_TABELA = CRIAR_TABELA_FORNECEDOR_ITEM

INSERIR = """
INSERT INTO fornecedor_item (id_fornecedor, id_item, observacoes, preco_personalizado, disponivel)
VALUES (?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE fornecedor_item
SET observacoes = ?, preco_personalizado = ?, disponivel = ?
WHERE id_fornecedor = ? AND id_item = ?;
"""

EXCLUIR = """
DELETE FROM fornecedor_item WHERE id_fornecedor = ? AND id_item = ?;
"""

OBTER_POR_CHAVE = """
SELECT id_fornecedor, id_item, observacoes, preco_personalizado, disponivel
FROM fornecedor_item WHERE id_fornecedor = ? AND id_item = ?;
"""

LISTAR_TODOS = """
SELECT id_fornecedor, id_item, observacoes, preco_personalizado, disponivel
FROM fornecedor_item ORDER BY id_fornecedor, id_item;
"""

# Queries específicas do domínio (mantidas para compatibilidade)
INSERIR_FORNECEDOR_ITEM = INSERIR
ATUALIZAR_FORNECEDOR_ITEM = ATUALIZAR

EXCLUIR_FORNECEDOR_ITEM = """
DELETE FROM fornecedor_item
WHERE id_fornecedor = ? AND id_item = ?;
"""

OBTER_FORNECEDOR_ITEM = """
SELECT id_fornecedor, id_item, observacoes, preco_personalizado, disponivel
FROM fornecedor_item
WHERE id_fornecedor = ? AND id_item = ?;
"""

OBTER_ITENS_POR_FORNECEDOR = """
SELECT fi.id_fornecedor, fi.id_item, fi.observacoes, fi.preco_personalizado, fi.disponivel,
       i.nome, i.descricao, i.preco, i.tipo
FROM fornecedor_item fi
JOIN item i ON fi.id_item = i.id
WHERE fi.id_fornecedor = ? AND fi.disponivel = 1;
"""

OBTER_FORNECEDORES_POR_ITEM = """
SELECT fi.id_fornecedor, fi.id_item, fi.observacoes, fi.preco_personalizado, fi.disponivel,
       u.nome as nome_fornecedor, u.email, u.telefone
FROM fornecedor_item fi
JOIN usuario u ON fi.id_fornecedor = u.id
WHERE fi.id_item = ? AND fi.disponivel = 1;
"""

OBTER_ITENS_POR_FORNECEDOR_E_TIPO = """
SELECT fi.id_fornecedor, fi.id_item, fi.observacoes, fi.preco_personalizado, fi.disponivel,
       i.nome, i.descricao, i.preco, i.tipo
FROM fornecedor_item fi
JOIN item i ON fi.id_item = i.id
WHERE fi.id_fornecedor = ? AND i.tipo = ? AND fi.disponivel = 1;
"""