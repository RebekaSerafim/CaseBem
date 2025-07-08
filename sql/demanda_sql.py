CRIAR_TABELA_DEMANDA = """
CREATE TABLE IF NOT EXISTS demanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,

"""

INSERIR_DEMANDA = """
INSERT INTO demanda (valor)
VALUES (?);
"""

ATUALIZAR_DEMANDA= """
UPDATE demanda
SET valor = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_DEMANDA = """
UPDATE demanda
SET tipo = ?
WHERE id = ?;
"""

EXCLUIR_DEMANDA = """
DELETE FROM demanda
WHERE id = ?;
"""

OBTER_DEMANDA_POR_ID = """
SELECT id, valor
FROM Contrato
WHERE id = ?;
"""

OBTER_DEMANDAS_POR_PAGINA = """
SELECT id, valor
FROM Contrato
ORDER BY id ASC
LIMIT ? OFFSET ?;
"""