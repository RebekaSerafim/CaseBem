CRIAR_TABELA_FAVORITO = """
CREATE TABLE IF NOT EXISTS favorito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_noivo INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_noivo, id_item)
);
"""

INSERIR_FAVORITO = """
INSERT INTO favorito (id_noivo, id_item)
VALUES (?, ?);
"""

EXCLUIR_FAVORITO = """
DELETE FROM favorito
WHERE id_noivo = ? AND id_item = ?;
"""

OBTER_FAVORITOS_POR_NOIVO = """
SELECT f.id, f.id_noivo, f.id_item, f.data_adicao,
       i.nome, i.descricao, i.preco, i.tipo, i.ativo,
       i.id_fornecedor
FROM favorito f
JOIN item i ON f.id_item = i.id
WHERE f.id_noivo = ? AND i.ativo = 1
ORDER BY f.data_adicao DESC;
"""

VERIFICAR_FAVORITO = """
SELECT COUNT(*) as count
FROM favorito
WHERE id_noivo = ? AND id_item = ?;
"""

CONTAR_FAVORITOS_POR_NOIVO = """
SELECT COUNT(*) as total
FROM favorito f
JOIN item i ON f.id_item = i.id
WHERE f.id_noivo = ? AND i.ativo = 1;
"""