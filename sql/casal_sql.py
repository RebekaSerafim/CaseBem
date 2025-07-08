CRIAR_TABELA_CASAL = """
CREATE TABLE IF NOT EXISTS Casal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_noivo1 INTEGER NOT NULL,
    id_noivo2 INTEGER NOT NULL,
    orcamento FLOAT NOT NULL,
    data_hora_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_noivo1) REFERENCES Usuario(id),
    FOREIGN KEY (id_noivo2) REFERENCES Usuario(id)
);
"""

INSERIR_CASAL = """
INSERT INTO Casal (id_noivo1, id_noivo2, orcamento)
VALUES (?, ?, ?);
"""

ATUALIZAR_CASAL = """
UPDATE Casal
SET orcamento = ?
WHERE id_casal = ?;
"""

EXCLUIR_CASAL = """
DELETE FROM Casal
WHERE id_casal = ?;
"""

OBTER_CASAL_POR_ID = """
SELECT id, id_noivo1, id_noivo2, orcamento
FROM Casal
WHERE id = ?;
"""

OBTER_CASAL_POR_NOIVO = """
SELECT id, id_noivo1, id_noivo2, orcamento
FROM Casal
WHERE (id_noivo1 = ? OR id_noivo2 = ?)
ORDER BY data_hora_cadastro DESC
"""

OBTER_CASAL_POR_PAGINA = """
SELECT id, id_noivo1, id_noivo2, orcamento
FROM Casal
LIMIT ? OFFSET ?;
"""
