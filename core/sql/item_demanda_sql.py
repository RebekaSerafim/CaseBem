"""
Queries SQL para a tabela item_demanda.

IMPORTANTE: A partir da refatoração V2, ItemDemanda NÃO tem vínculo com
um item específico do catálogo. É uma descrição livre do que o noivo quer.

Estrutura:
- id: PK auto-increment
- id_demanda: FK para demanda
- tipo: VARCHAR(20) - PRODUTO, SERVICO ou ESPACO
- id_categoria: FK para categoria
- descricao: TEXT - descrição livre do que o noivo quer
- quantidade: INTEGER
- preco_maximo: REAL (opcional)
- observacoes: TEXT (opcional)
"""

CRIAR_TABELA_ITEM_DEMANDA = """
CREATE TABLE IF NOT EXISTS item_demanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_demanda INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    id_categoria INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_maximo REAL,
    observacoes TEXT,
    FOREIGN KEY (id_demanda) REFERENCES demanda(id) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);
"""

# Queries compatíveis com BaseRepo
CRIAR_TABELA = CRIAR_TABELA_ITEM_DEMANDA

INSERIR = """
INSERT INTO item_demanda (id_demanda, tipo, id_categoria, descricao, quantidade, preco_maximo, observacoes)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE item_demanda
SET tipo = ?, id_categoria = ?, descricao = ?, quantidade = ?, preco_maximo = ?, observacoes = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM item_demanda
WHERE id = ?;
"""

OBTER_POR_CHAVE = """
SELECT id, id_demanda, tipo, id_categoria, descricao, quantidade, preco_maximo, observacoes
FROM item_demanda
WHERE id = ?;
"""

OBTER_POR_ID = OBTER_POR_CHAVE

LISTAR_TODOS = """
SELECT id, id_demanda, tipo, id_categoria, descricao, quantidade, preco_maximo, observacoes
FROM item_demanda
ORDER BY id_demanda, id;
"""

# Queries específicas do domínio

OBTER_ITENS_POR_DEMANDA = """
SELECT
    id.id,
    id.id_demanda,
    id.tipo,
    id.id_categoria,
    id.descricao,
    id.quantidade,
    id.preco_maximo,
    id.observacoes,
    c.nome as categoria_nome
FROM item_demanda id
LEFT JOIN categoria c ON id.id_categoria = c.id
WHERE id.id_demanda = ?
ORDER BY id.id;
"""

OBTER_POR_TIPO_E_CATEGORIA = """
SELECT
    id.id,
    id.id_demanda,
    id.tipo,
    id.id_categoria,
    id.descricao,
    id.quantidade,
    id.preco_maximo,
    id.observacoes,
    c.nome as categoria_nome
FROM item_demanda id
LEFT JOIN categoria c ON id.id_categoria = c.id
WHERE id.tipo = ? AND id.id_categoria = ?
ORDER BY id.id_demanda, id.id;
"""

CONTAR_POR_DEMANDA = """
SELECT COUNT(*) as total
FROM item_demanda
WHERE id_demanda = ?;
"""

EXCLUIR_ITENS_POR_DEMANDA = """
DELETE FROM item_demanda
WHERE id_demanda = ?;
"""

# Buscar demandas que têm itens de determinado tipo e categoria (para fornecedores)
OBTER_DEMANDAS_COM_ITENS_COMPATIVEIS = """
SELECT DISTINCT id_demanda
FROM item_demanda
WHERE tipo = ? AND id_categoria IN ({categorias_placeholder});
"""
