CRIAR_TABELA_DEMANDA = """
CREATE TABLE IF NOT EXISTS demanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_casal INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    orcamento_min DECIMAL(10,2),
    orcamento_max DECIMAL(10,2),
    prazo_entrega VARCHAR(255),
    status VARCHAR(20) DEFAULT 'ATIVA',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT,
    FOREIGN KEY (id_casal) REFERENCES casal(id),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);
"""

INSERIR_DEMANDA = """
INSERT INTO demanda (id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, observacoes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_DEMANDA = """
UPDATE demanda
SET titulo = ?, descricao = ?, orcamento_min = ?, orcamento_max = ?, prazo_entrega = ?, observacoes = ?
WHERE id = ?;
"""

ATUALIZAR_STATUS_DEMANDA = """
UPDATE demanda
SET status = ?
WHERE id = ?;
"""

EXCLUIR_DEMANDA = """
DELETE FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDA_POR_ID = """
SELECT id, id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDAS_POR_PAGINA = """
SELECT id, id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, status, data_criacao, observacoes
FROM demanda
ORDER BY data_criacao DESC
LIMIT ? OFFSET ?;
"""

OBTER_DEMANDAS_POR_CASAL = """
SELECT id, id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE id_casal = ?
ORDER BY data_criacao DESC;
"""

OBTER_DEMANDAS_ATIVAS = """
SELECT id, id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE status = 'ATIVA'
ORDER BY data_criacao DESC;
"""

BUSCAR_DEMANDAS = """
SELECT id, id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE (titulo LIKE ? OR descricao LIKE ?) AND status = 'ATIVA'
ORDER BY data_criacao DESC;
"""

OBTER_DEMANDAS_POR_STATUS = """
SELECT id, id_casal, id_categoria, titulo, descricao, orcamento_min, orcamento_max, prazo_entrega, status, data_criacao, observacoes
FROM demanda
WHERE status = ?
ORDER BY data_criacao DESC;
"""