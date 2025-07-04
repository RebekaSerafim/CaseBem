CRIAR_TABELA_FORNECEDOR_PRODUTO = """
CREATE TABLE IF NOT EXISTS FornecedorProduto (
    idFornecedor INTEGER NOT NULL,
    idProduto INTEGER NOT NULL,
    observacoes VARCHAR(255),
    preco FLOAT,
    PRIMARY KEY (idFornecedor, idProduto),
    FOREIGN KEY (idFornecedor) REFERENCES Fornecedor(id),
    FOREIGN KEY (idProduto) REFERENCES Produto(id)
);
"""

INSERIR_FORNECEDOR_PRODUTO = """
INSERT INTO FornecedorProduto (idFornecedor, idProduto, observacoes, preco)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_FORNECEDOR_PRODUTO = """
UPDATE FornecedorProduto
SET observacoes = ?, preco = ?
WHERE idFornecedor = ? AND idProduto = ?;
"""

EXCLUIR_FORNECEDOR_PRODUTO = """
DELETE FROM FornecedorProduto
WHERE idFornecedor = ? AND idProduto = ?;
"""

OBTER_FORNECEDOR_PRODUTO_POR_ID = """
SELECT idFornecedor, idProduto, observacoes, preco
FROM FornecedorProduto
WHERE idFornecedor = ? AND idProduto = ?;
"""

OBTER_FORNECEDORES_PRODUTO_POR_PAGINA = """
SELECT idFornecedor, idProduto, observacoes, preco
FROM FornecedorProduto
ORDER BY idFornecedor ASC
LIMIT ? OFFSET ?;
"""
