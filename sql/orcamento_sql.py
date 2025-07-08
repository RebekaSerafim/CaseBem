CRIAR_TABELA_ORCAMENTO = """
CREATE TABLE IF NOT EXISTS orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_demanda INTEGER NOT NULL,
    id_fornecedor_prestador INTEGER NOT NULL,
    data_hora_cadastro TIMESTAMP NOT NULL,
    data_hora_validade TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'PENDENTE',
    observacoes TEXT,
    valor_total REAL,
    FOREIGN KEY (id_demanda) REFERENCES demanda(id) ON DELETE CASCADE,
    FOREIGN KEY (id_fornecedor_prestador) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR_ORCAMENTO = """
INSERT INTO orcamento (id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
                      data_hora_validade, status, observacoes, valor_total)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_ORCAMENTO = """
UPDATE orcamento
SET data_hora_validade = ?, status = ?, observacoes = ?, valor_total = ?
WHERE id = ?;
"""

ATUALIZAR_STATUS_ORCAMENTO = """
UPDATE orcamento
SET status = ?
WHERE id = ?;
"""

ATUALIZAR_VALOR_TOTAL_ORCAMENTO = """
UPDATE orcamento
SET valor_total = ?
WHERE id = ?;
"""

EXCLUIR_ORCAMENTO = """
DELETE FROM orcamento
WHERE id = ?;
"""

OBTER_ORCAMENTO_POR_ID = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE id = ?;
"""

OBTER_ORCAMENTOS_POR_DEMANDA = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE id_demanda = ?
ORDER BY data_hora_cadastro DESC;
"""

OBTER_ORCAMENTOS_POR_FORNECEDOR_PRESTADOR = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE id_fornecedor_prestador = ?
ORDER BY data_hora_cadastro DESC;
"""

OBTER_ORCAMENTOS_POR_STATUS = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
WHERE status = ?
ORDER BY data_hora_cadastro DESC;
"""

OBTER_ORCAMENTOS_POR_PAGINA = """
SELECT id, id_demanda, id_fornecedor_prestador, data_hora_cadastro, 
       data_hora_validade, status, observacoes, valor_total
FROM orcamento
ORDER BY data_hora_cadastro DESC
LIMIT ? OFFSET ?;
"""

# Query específica para aceitar um orçamento e rejeitar outros da mesma demanda
ACEITAR_ORCAMENTO_E_REJEITAR_OUTROS = """
UPDATE orcamento
SET status = CASE
    WHEN id = ? THEN 'ACEITO'
    ELSE 'REJEITADO'
END
WHERE id_demanda = ? AND status = 'PENDENTE';
"""