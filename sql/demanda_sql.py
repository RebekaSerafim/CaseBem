CRIAR_TABELA_DEMANDA = """
CREATE TABLE IF NOT EXISTS demanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_casal INTEGER NOT NULL,
    data_hora_cadastro TIMESTAMP NOT NULL,
    FOREIGN KEY (id_casal) REFERENCES casal(id) ON DELETE CASCADE
);
"""

INSERIR_DEMANDA = """
INSERT INTO demanda (id_casal, data_hora_cadastro)
VALUES (?, ?);
"""

ATUALIZAR_DEMANDA = """
UPDATE demanda
SET id_casal = ?, data_hora_cadastro = ?
WHERE id = ?;
"""

EXCLUIR_DEMANDA = """
DELETE FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDA_POR_ID = """
SELECT id, id_casal, data_hora_cadastro
FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDAS_POR_PAGINA = """
SELECT id, id_casal, data_hora_cadastro
FROM demanda
ORDER BY data_hora_cadastro DESC
LIMIT ? OFFSET ?;
"""

OBTER_DEMANDAS_POR_CASAL = """
SELECT id, id_casal, data_hora_cadastro
FROM demanda
WHERE id_casal = ?
ORDER BY data_hora_cadastro DESC;
"""