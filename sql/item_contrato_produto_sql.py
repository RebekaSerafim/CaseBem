CRIAR_TABELA_ITEM_CONTRATO_PRODUTO = """
CREATE TABLE IF NOT EXISTS ItemContratoProduto (
    idItemContratoProduto INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL,
    quantidade INTEGER,
    idProduto INTEGER NOT NULL,
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
);
"""

INSERIR_ITEM_CONTRATO_PRODUTO = """
INSERT INTO ItemContratoProduto (valor, quantidade, idProduto)
VALUES (?, ?, ?);
"""

ATUALIZAR_ITEM_CONTRATO_PRODUTO = """
UPDATE ItemContratoProduto
SET valor = ?, quantidade = ?, idProduto = ?
WHERE idItemContratoProduto = ?;
"""

EXCLUIR_ITEM_CONTRATO_PRODUTO = """
DELETE FROM ItemContratoProduto
WHERE idItemContratoProduto = ?;
"""

OBTER_ITEM_CONTRATO_PRODUTO_POR_ID = """
SELECT idItemContratoProduto, valor, quantidade, idProduto
FROM ItemContratoProduto
WHERE idItemContratoProduto = ?;
"""

OBTER_ITENS_CONTRATO_PRODUTO = """
SELECT idItemContratoProduto, valor, quantidade, idProduto
FROM ItemContratoProduto
ORDER BY idItemContratoProduto ASC
LIMIT ? OFFSET ?;
"""
