CRIAR_TABELA_NOIVO = """
CREATE TABLE IF NOT EXISTS Noivo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orcamento FLOAT NOT NULL,
    id_noivo1 TEXT NOT NULL,
    id_noivo2 TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('ADMIN', 'NOIVO', 'PRESTADOR', 'FORNECEDOR'))
);
"""

INSERIR_NOIVO = """
INSERT INTO Noivo (orcamento, id_noivo1, id_noivo2)
VALUES (?, ?, ?);
"""

ATUALIZAR_NOIVO = """
UPDATE Noivo
SET orcamento = ?, id_noivo1 = ?, id_noivo2 = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_NOIVO = """
UPDATE Noivo
SET tipo = ?
WHERE id = ?;
"""

EXCLUIR_NOIVO = """
DELETE FROM Noivo
WHERE id = ?;
"""

OBTER_NOIVO_POR_ID = """
SELECT id, orcamento, id_noivo1, id_noivo2, tipo
FROM Noivo
WHERE id = ?;
"""

OBTER_NOIVO_POR_PAGINA = """
SELECT id, orcamento, id_noivo1, id_noivo2
FROM Noivo
ORDER BY id ASC
LIMIT ? OFFSET ?;
"""
