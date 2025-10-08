CRIAR_TABELA_ITEM_ORCAMENTO = """
CREATE TABLE IF NOT EXISTS item_orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orcamento INTEGER NOT NULL,
    id_item_demanda INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_unitario REAL NOT NULL,
    observacoes TEXT,
    desconto REAL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'PENDENTE',
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id) ON DELETE CASCADE,
    FOREIGN KEY (id_item_demanda) REFERENCES item_demanda(id) ON DELETE CASCADE,
    FOREIGN KEY (id_item) REFERENCES item(id) ON DELETE CASCADE,
    UNIQUE(id_orcamento, id_item_demanda, id_item)
);
"""

# Queries compatíveis com BaseRepo
CRIAR_TABELA = CRIAR_TABELA_ITEM_ORCAMENTO

INSERIR = """
INSERT INTO item_orcamento (id_orcamento, id_item_demanda, id_item, quantidade, preco_unitario, observacoes, desconto, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE item_orcamento
SET id_item_demanda = ?, id_item = ?, quantidade = ?, preco_unitario = ?, observacoes = ?, desconto = ?, status = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM item_orcamento
WHERE id = ?;
"""

OBTER_POR_ID = """
SELECT id, id_orcamento, id_item_demanda, id_item, quantidade, preco_unitario, observacoes, desconto, status
FROM item_orcamento
WHERE id = ?;
"""

LISTAR_TODOS = """
SELECT id, id_orcamento, id_item_demanda, id_item, quantidade, preco_unitario, observacoes, desconto, status
FROM item_orcamento
ORDER BY id_orcamento, id_item_demanda, id;
"""

# Queries específicas do domínio
OBTER_ITENS_POR_ORCAMENTO = """
SELECT
    io.id,
    io.id_orcamento,
    io.id_item_demanda,
    io.id_item,
    io.quantidade,
    io.preco_unitario,
    io.observacoes,
    io.desconto,
    io.status,
    i.nome as item_nome,
    i.descricao as item_descricao,
    i.preco as item_preco,
    i.tipo as item_tipo,
    i.id_categoria as item_id_categoria,
    id.descricao as item_demanda_descricao,
    id.quantidade as item_demanda_quantidade,
    id.preco_maximo as item_demanda_preco_maximo,
    c.nome as categoria_nome,
    (io.quantidade * io.preco_unitario - COALESCE(io.desconto, 0)) as preco_total
FROM item_orcamento io
JOIN item i ON io.id_item = i.id
JOIN item_demanda id ON io.id_item_demanda = id.id
LEFT JOIN categoria c ON id.id_categoria = c.id
WHERE io.id_orcamento = ?
ORDER BY io.id_item_demanda, io.id;
"""

OBTER_ITENS_POR_ITEM_DEMANDA = """
SELECT
    io.id,
    io.id_orcamento,
    io.id_item_demanda,
    io.id_item,
    io.quantidade,
    io.preco_unitario,
    io.observacoes,
    io.desconto,
    io.status,
    i.nome as item_nome,
    (io.quantidade * io.preco_unitario - COALESCE(io.desconto, 0)) as preco_total
FROM item_orcamento io
JOIN item i ON io.id_item = i.id
WHERE io.id_orcamento = ? AND io.id_item_demanda = ?
ORDER BY io.id;
"""

OBTER_TOTAL_ORCAMENTO = """
SELECT SUM(quantidade * preco_unitario - COALESCE(desconto, 0)) as total
FROM item_orcamento
WHERE id_orcamento = ? AND status = 'ACEITO';
"""

EXCLUIR_ITENS_POR_ORCAMENTO = """
DELETE FROM item_orcamento
WHERE id_orcamento = ?;
"""

VERIFICAR_ITEM_JA_USADO = """
SELECT COUNT(*) as count
FROM item_orcamento
WHERE id_orcamento = ? AND id_item_demanda = ? AND id_item = ?;
"""

OBTER_ITENS_USADOS_PARA_ITEM_DEMANDA = """
SELECT DISTINCT id_item
FROM item_orcamento
WHERE id_orcamento = ? AND id_item_demanda = ?;
"""

# Novas queries para gestão de status individual
ATUALIZAR_STATUS_ITEM = """
UPDATE item_orcamento
SET status = ?
WHERE id = ?;
"""

OBTER_ITENS_POR_STATUS = """
SELECT
    io.id,
    io.id_orcamento,
    io.id_item_demanda,
    io.id_item,
    io.quantidade,
    io.preco_unitario,
    io.observacoes,
    io.desconto,
    io.status,
    i.nome as item_nome,
    i.descricao as item_descricao,
    i.tipo as item_tipo,
    (io.quantidade * io.preco_unitario - COALESCE(io.desconto, 0)) as preco_total
FROM item_orcamento io
JOIN item i ON io.id_item = i.id
WHERE io.id_orcamento = ? AND io.status = ?
ORDER BY io.id;
"""

CONTAR_ITENS_POR_STATUS = """
SELECT COUNT(*) as total
FROM item_orcamento
WHERE id_orcamento = ? AND status = ?;
"""

VERIFICAR_ITEM_DEMANDA_JA_ACEITO = """
SELECT COUNT(*) as count
FROM item_orcamento
WHERE id_item_demanda = ? AND status = 'ACEITO';
"""