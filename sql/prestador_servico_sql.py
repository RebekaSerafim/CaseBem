CRIAR_TABELA_PRESTADOR_SERVICO = """
CREATE TABLE IF NOT EXISTS prestador_servico (
    id_prestador INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    observacoes TEXT NOT NULL,
    preco REAL,
    PRIMARY KEY (id_prestador, id_servico),
    FOREIGN KEY (id_prestador) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id) ON DELETE CASCADE
);
"""

INSERIR_PRESTADOR_SERVICO = """
INSERT INTO prestador_servico (id_prestador, id_servico, observacoes, preco)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR_PRESTADOR_SERVICO = """
UPDATE prestador_servico
SET observacoes = ?, preco = ?
WHERE id_prestador = ? AND id_servico = ?;
"""

EXCLUIR_PRESTADOR_SERVICO = """
DELETE FROM prestador_servico
WHERE id_prestador = ? AND id_servico = ?;
"""

OBTER_PRESTADOR_SERVICO_POR_ID = """
SELECT id_prestador, id_servico, observacoes, preco
FROM prestador_servico
WHERE id_prestador = ? AND id_servico = ?;
"""

OBTER_PRESTADORES_SERVICO_POR_PAGINA = """
SELECT id_prestador, id_servico, observacoes, preco
FROM prestador_servico
ORDER BY id_prestador ASC
LIMIT ? OFFSET ?;
"""