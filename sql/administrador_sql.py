CRIAR_TABELA_ADMINISTRADOR = """
CREATE TABLE IF NOT EXISTS Administrador (
    id_administrador INTEGER PRIMARY KEY,
    FOREIGN KEY (id_administrador) REFERENCES Usuario(id)
);
"""

INSERIR_ADMINISTRADOR = """
INSERT INTO Administrador(id_administrador)
VALUES (?);
"""

ATUALIZAR_ADMINISTRADOR = """
UPDATE Administrador
SET id_administrador = ?
WHERE id_administrador = ?;
"""

EXCLUIR_ADMINISTRADOR = """
DELETE FROM Administrador
WHERE id_administrador = ?;
"""

OBTER_ADMINISTRADOR_POR_ID = """
SELECT a.id_administrador, u.nome, u.telefone, u.email, u.senha_hash, u.tipo
FROM Administrador a
JOIN Usuario u ON a.id_administrador = u.id
WHERE a.id_administrador = ?;
"""

OBTER_ADMINISTRADORES_POR_PAGINA = """
SELECT a.id_administrador, u.nome, u.telefone, u.email, u.senha_hash, u.tipo
FROM Administrador a
JOIN Usuario u ON a.id_administrador = u.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""