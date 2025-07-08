CRIAR_TABELA_CONTRATO = """
CREATE TABLE IF NOT EXISTS contrato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,

"""

INSERIR_CONTRATO = """
INSERT INTO contrato (valor)
VALUES (?);
"""

ATUALIZAR_CONTRATO= """
UPDATE contrato
SET valor = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_CONTRATO = """
UPDATE contrato
SET tipo = ?
WHERE id = ?;
"""



EXCLUIR_CONTRATO = """
DELETE FROM contrato
WHERE id = ?;
"""

OBTER_CONTRATO_POR_ID = """
SELECT id, valor
FROM Contrato
WHERE id = ?;
"""




OBTER_CONTRATOS_POR_PAGINA = """
SELECT id, valor
FROM Contrato
ORDER BY id ASC
LIMIT ? OFFSET ?;
"""