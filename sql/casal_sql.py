CRIAR_TABELA_CASAL = """
CREATE TABLE IF NOT EXISTS casal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_noivo1 INTEGER NOT NULL,
    id_noivo2 INTEGER NOT NULL,
    data_casamento TEXT,
    local_previsto TEXT,
    orcamento TEXT,
    numero_convidados INTEGER,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_noivo1) REFERENCES usuario(id),
    FOREIGN KEY (id_noivo2) REFERENCES usuario(id)
);
"""

INSERIR_CASAL = """
INSERT INTO casal (id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento, numero_convidados)
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR_CASAL = """
UPDATE casal
SET data_casamento = ?, local_previsto = ?, orcamento = ?, numero_convidados = ?
WHERE id = ?;
"""

EXCLUIR_CASAL = """
DELETE FROM casal
WHERE id = ?;
"""

OBTER_CASAL_POR_ID = """
SELECT id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento, numero_convidados, data_cadastro
FROM casal
WHERE id = ?;
"""

OBTER_CASAL_POR_NOIVO = """
SELECT id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento, numero_convidados, data_cadastro
FROM casal
WHERE (id_noivo1 = ? OR id_noivo2 = ?)
ORDER BY id DESC;
"""

OBTER_CASAL_POR_PAGINA = """
SELECT id, id_noivo1, id_noivo2, data_casamento, local_previsto, orcamento, numero_convidados, data_cadastro
FROM casal
LIMIT ? OFFSET ?;
"""
