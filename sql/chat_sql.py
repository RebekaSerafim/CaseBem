CRIAR_TABELA_CHAT = """
CREATE TABLE IF NOT EXISTS Chat (
    idRemetente INTEGER NOT NULL,
    idDestinatario INTEGER NOT NULL,
    mensagem VARCHAR(256) NOT NULL,
    dataHoraEnvio DATETIME NOT NULL,
    dataHoraLeitura DATETIME,
    FOREIGN KEY (idRemetente) REFERENCES Usuario(id),
    FOREIGN KEY (idDestinatario) REFERENCES Usuario(id)
);
"""

INSERIR_CHAT = """
INSERT INTO Chat (idRemetente, idDestinatario, mensagem, dataHoraEnvio, dataHoraLeitura)
VALUES (?, ?, ?, ?, ?);
"""

OBTER_MENSAGENS_POR_USUARIO = """
SELECT idRemetente, idDestinatario, mensagem, dataHoraEnvio, dataHoraLeitura
FROM Chat
WHERE idRemetente = ? OR idDestinatario = ?
ORDER BY dataHoraEnvio DESC
LIMIT ? OFFSET ?;
"""

ATUALIZAR_DATA_LEITURA = """
UPDATE Chat
SET dataHoraLeitura = ?
WHERE idRemetente = ? AND idDestinatario = ? AND dataHoraEnvio = ?;
"""
