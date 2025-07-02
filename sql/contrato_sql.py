CRIAR_TABELA_CONTRATO = """
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,

"""

INSERIR_CONTRATO = """
INSERT INTO servico (valor)
VALUES (?);
"""

ATUALIZAR_CONTRATO= """
UPDATE servico
SET valor = ?
WHERE id = ?;
"""

ATUALIZAR_TIPO_CONTRATO = """
UPDATE servico
SET tipo = ?
WHERE id = ?;
"""



EXCLUIR_CONTRATO = """
DELETE FROM servico
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