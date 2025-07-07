CRIAR_TABELA_CASAL = """
CREATE TABLE IF NOT EXISTS Casal (    
    id_noivo1 INTEGER NOT NULL,
    id_noivo2 INTEGER NOT NULL,
    orcamento FLOAT NOT NULL,
    PRIMARY KEY (id_noivo1, id_noivo2),
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
WHERE id_noivo1 = ? AND id_noivo2 = ?;
"""

EXCLUIR_CASAL = """
DELETE FROM Casal
WHERE id_noivo1 = ? AND id_noivo2 = ?;
"""

OBTER_CASAL_POR_IDS = """
SELECT id_noivo1, id_noivo2, orcamento
FROM Casal
WHERE id_noivo1 = ? AND id_noivo2 = ?;
"""

OBTER_CASAL_POR_PAGINA = """
SELECT id_noivo1, id_noivo2, orcamento
FROM Casal
LIMIT ? OFFSET ?;
"""
