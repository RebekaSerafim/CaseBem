# ==============================================================================
# QUERIES GENÉRICAS (usadas pelo BaseRepo)
# ==============================================================================

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS casal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_noivo1 INTEGER NOT NULL,
    id_noivo2 INTEGER NOT NULL,
    data_casamento TEXT,
    local_previsto TEXT,
    orcamento_estimado TEXT,
    numero_convidados INTEGER,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_noivo1) REFERENCES usuario(id),
    FOREIGN KEY (id_noivo2) REFERENCES usuario(id)
);
"""

INSERIR = """
INSERT INTO casal (id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento_estimado, numero_convidados)
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE casal
SET data_casamento = ?, local_previsto = ?, orcamento_estimado = ?, numero_convidados = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM casal
WHERE id = ?;
"""

OBTER_POR_ID = """
SELECT id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento_estimado, numero_convidados, data_cadastro
FROM casal
WHERE id = ?;
"""

LISTAR_TODOS = """
SELECT id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento_estimado, numero_convidados, data_cadastro
FROM casal
ORDER BY id DESC;
"""

# ==============================================================================
# QUERIES ESPECÍFICAS DE NEGÓCIO (métodos customizados do repositório)
# ==============================================================================

# Alias mantido para compatibilidade com método obter_por_id_completo()
OBTER_CASAL_POR_ID = OBTER_POR_ID

OBTER_CASAL_POR_NOIVO = """
SELECT id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento_estimado, numero_convidados, data_cadastro
FROM casal
WHERE (id_noivo1 = ? OR id_noivo2 = ?)
ORDER BY id DESC;
"""

# Query OBTER_CASAL_POR_PAGINA removida: Use BaseRepo.obter_paginado() ao invés
