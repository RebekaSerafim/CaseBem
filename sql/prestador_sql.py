CRIAR_TABELA_PRESTADOR = """
CREATE TABLE IF NOT EXISTS Prestador (
    id_prestador INTEGER PRIMARY,
    tipo_pessoa TEXT NOT NULL CHECK(tipo_pessoa IN ('FISICA', 'JURIDICA')),
    documento TEXT NOT NULL UNIQUE,
    FOREIGN KEY (id_prestador) REFERENCES Usuario(id);
"""

INSERIR_PRESTADOR = """
INSERT INTO Prestador(id_prestador, tipo_pessoa, documento)
VALUES (?, ?, ?);
"""

ATUALIZAR_PRESTADOR = """
UPDATE Prestador
SET tipo_pessoa = ?, documento = ?
WHERE id_prestador = ?;
"""

EXCLUIR_PRESTADOR = """
DELETE FROM Prestador
WHERE id_prestador = ?;
"""

OBTER_PRESTADOR_POR_ID = """
SELECT p.id_prestador, u.nome, u.telefone, u.email, u.senha_hash, p.tipo, p.tipo_pessoa, p.documento
FROM Prestador p
JOIN Usuario u ON p.id_prestador = u.id
WHERE p.id_prestador = ?;
"""

OBTER_PRESTADOR_POR_EMAIL = """
SELECT p.id_prestador, u.nome, u.telefone, u.email, u.senha_hash, p.tipo, p.tipo_pessoa, p.documento
FROM Prestador p
JOIN Usuario u ON p.id_prestador = u.id
WHERE u.email = ?;
"""

OBTER_PRESTADORES_POR_PAGINA = """
SELECT p.id_prestador, u.nome, u.telefone, u.email, u.senha_hash, p.tipo, p.tipo_pessoa, p.documento
FROM Prestador p
JOIN Usuario u ON p.id_prestador = u.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""