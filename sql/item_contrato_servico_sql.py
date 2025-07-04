CRIAR_TABELA_ITEM_CONTRATO_SERVICO = """
CREATE TABLE IF NOT EXISTS ItemContratoServico (
    idItemContratoServico INTEGER PRIMARY KEY AUTOINCREMENT,
    valor FLOAT,
    quantidade INTEGER,
    idServico INTEGER NOT NULL,
    FOREIGN KEY (idServico) REFERENCES Servico(id)
);
"""

INSERIR_ITEM_CONTRATO_SERVICO = """
INSERT INTO ItemContratoServico (valor, quantidade, idServico)
VALUES (?, ?, ?);
"""

ATUALIZAR_ITEM_CONTRATO_SERVICO = """
UPDATE ItemContratoServico
SET valor = ?, quantidade = ?, idServico = ?
WHERE idItemContratoServico = ?;
"""

EXCLUIR_ITEM_CONTRATO_SERVICO = """
DELETE FROM ItemContratoServico
WHERE idItemContratoServico = ?;
"""

OBTER_ITEM_CONTRATO_SERVICO_POR_ID = """
SELECT idItemContratoServico, valor, quantidade, idServico
FROM ItemContratoServico
WHERE idItemContratoServico = ?;
"""

OBTER_ITENS_CONTRATO_SERVICO_POR_PAGINA = """
SELECT idItemContratoServico, valor, quantidade, idServico
FROM ItemContratoServico
ORDER BY idItemContratoServico ASC
LIMIT ? OFFSET ?;
"""
