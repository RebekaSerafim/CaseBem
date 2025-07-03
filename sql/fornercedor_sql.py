CRIAR_TABELA_FORNECEDOR = """
CREATE TABLE IF NOT EXISTS Administrador (
    id_fornecedor INTEGER PRIMARY KEY,
    FOREIGN KEY (id_fornecedor) REFERENCES Usuario(id)
);
"""

INSERIR_FORNECEDOR = """
INSERT INTO Fornecedor(id_fornecedor)
VALUES (?);
"""

ATUALIZAR_FORNECEDOR = """
UPDATE Fornecedor
SET id_fornecedor = ?
WHERE id_fornecedor = ?;
"""

EXCLUIR_FORNECEDOR = """
DELETE FROM Fornecedor
WHERE id_fornecedor = ?;
"""

OBTER_FORNECEDOR_POR_ID = """
SELECT a.id_fornecedor, u.nome, u.telefone, u.email, u.senha_hash, u.tipo
FROM Fornecedor f
JOIN Usuario u ON a.id_fornecedor = u.id
WHERE a.id_fornecedor = ?;
"""

OBTER_FORNECEDORES_POR_PAGINA = """
SELECT a.id_fornecedor, u.nome, u.telefone, u.email, u.senha_hash, u.tipo
FROM Fornecedor f
JOIN Usuario u ON a.id_fornecedor = u.id
ORDER BY u.nome ASC
LIMIT ? OFFSET ?;
"""