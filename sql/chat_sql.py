CRIAR_TABELA_CHAT = """
CREATE TABLE IF NOT EXISTS chat (
    id_remetente INTEGER NOT NULL,
    id_destinatario INTEGER NOT NULL,
    data_hora_envio TIMESTAMP NOT NULL,
    mensagem TEXT NOT NULL,
    data_hora_leitura TIMESTAMP,
    PRIMARY KEY (id_remetente, id_destinatario, data_hora_envio),
    FOREIGN KEY (id_remetente) REFERENCES usuario(id),
    FOREIGN KEY (id_destinatario) REFERENCES usuario(id)
);
"""

INSERIR_CHAT = """
INSERT INTO chat (id_remetente, id_destinatario, data_hora_envio, mensagem)
VALUES (?, ?, ?, ?);
"""

OBTER_MENSAGENS_POR_USUARIO = """
SELECT id_remetente, id_destinatario, data_hora_envio, mensagem, data_hora_leitura
FROM chat
WHERE id_remetente = ? OR id_destinatario = ?
ORDER BY data_hora_envio DESC
LIMIT ? OFFSET ?;
"""

ATUALIZAR_DATA_LEITURA = """
UPDATE chat
SET data_hora_leitura = ?
WHERE id_remetente = ? AND id_destinatario = ? AND data_hora_envio = ?;
"""
