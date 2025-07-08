from typing import List
from datetime import datetime
from util.database import obter_conexao
from sql.chat_sql import *
from model.chat_model import Chat

def criar_tabela_chat() -> bool:
    try:
        with obter_conexao() as conexao:
            conexao.execute(CRIAR_TABELA_CHAT)
        return True
    except Exception as e:
        print(f"Erro ao criar tabela Chat: {e}")
        return False

def inserir_chat(chat: Chat) -> bool:
    with obter_conexao() as conexao:
        conexao.execute(
            INSERIR_CHAT,
            (chat.id_remetente, chat.id_destinatario, chat.mensagem, chat.data_hora_envio, chat.data_hora_leitura)
        )
        return True

def obter_mensagens_por_usuario(id_usuario: int, pagina: int, tamanho: int) -> List[Chat]:
    offset = (pagina - 1) * tamanho
    with obter_conexao() as conexao:
        cursor = conexao.execute(OBTER_MENSAGENS_POR_USUARIO, (id_usuario, id_usuario, tamanho, offset))
        resultados = cursor.fetchall()
        return [Chat(
            id_remetente=r["idRemetente"],
            id_destinatario=r["idDestinatario"],
            mensagem=r["mensagem"],
            data_hora_envio=r["dataHoraEnvio"],
            data_hora_leitura=r["dataHoraLeitura"]
        ) for r in resultados]

def atualizar_data_leitura(id_remetente: int, id_destinatario: int, data_envio: datetime, data_leitura: datetime) -> bool:
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            ATUALIZAR_DATA_LEITURA,
            (data_leitura, id_remetente, id_destinatario, data_envio)
        )
        return cursor.rowcount > 0
