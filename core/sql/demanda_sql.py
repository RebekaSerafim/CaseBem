"""
Queries SQL para a tabela demanda.

REFATORAÇÃO V2:
- Removido: id_categoria (cada item tem sua própria categoria)
- Removido: orcamento_min e orcamento_max
- Removido: titulo (redundante, descrição já existe)
- Adicionado: orcamento_total (orçamento total da demanda)
- Adicionado: data_casamento (preenchido automaticamente do casal)
- Adicionado: cidade_casamento (preenchido automaticamente do casal)
"""

# ==============================================================================
# QUERIES GENÉRICAS (usadas pelo BaseRepo)
# ==============================================================================

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS demanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_casal INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    orcamento_total DECIMAL(10,2),
    data_casamento DATE,
    cidade_casamento VARCHAR(255),
    prazo_entrega VARCHAR(255),
    status VARCHAR(20) DEFAULT 'ATIVA',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT,
    FOREIGN KEY (id_casal) REFERENCES casal(id)
);
"""

INSERIR = """
INSERT INTO demanda (id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, observacoes)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE demanda
SET descricao = ?, orcamento_total = ?, data_casamento = ?, cidade_casamento = ?, prazo_entrega = ?, observacoes = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM demanda WHERE id = ?;
"""

OBTER_POR_ID = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE id = ?;
"""

LISTAR_TODOS = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
ORDER BY data_criacao DESC;
"""

# ==============================================================================
# QUERIES ESPECÍFICAS DE NEGÓCIO (métodos customizados do repositório)
# ==============================================================================

ATUALIZAR_STATUS_DEMANDA = """
UPDATE demanda
SET status = ?
WHERE id = ?;
"""

OBTER_DEMANDAS_POR_CASAL = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE id_casal = ?
ORDER BY data_criacao DESC;
"""

OBTER_DEMANDAS_ATIVAS = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE status = 'ATIVA'
ORDER BY data_criacao DESC;
"""

BUSCAR_DEMANDAS = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE (descricao LIKE ? OR observacoes LIKE ?) AND status = 'ATIVA'
ORDER BY data_criacao DESC;
"""

OBTER_DEMANDAS_POR_STATUS = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE status = ?
ORDER BY data_criacao DESC;
"""

# Buscar demandas por cidade (útil para fornecedores que atendem regiões específicas)
OBTER_DEMANDAS_POR_CIDADE = """
SELECT id, id_casal, descricao, orcamento_total, data_casamento, cidade_casamento, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE cidade_casamento = ? AND status = 'ATIVA'
ORDER BY data_criacao DESC;
"""
