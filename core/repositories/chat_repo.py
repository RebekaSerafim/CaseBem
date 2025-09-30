from typing import List
from datetime import datetime
from util.database import obter_conexao
from core.sql import chat_sql
from core.models.chat_model import Chat

class ChatRepo:
    """Repositório para operações com chat"""

    def __init__(self):
        self.nome_tabela = 'chat'

    def criar_tabela(self) -> bool:
        """Cria a tabela chat"""
        try:
            with obter_conexao() as conexao:
                conexao.execute(chat_sql.CRIAR_TABELA_CHAT)
            return True
        except Exception as e:
            print(f"Erro ao criar tabela Chat: {e}")
            return False

    def inserir(self, chat: Chat) -> bool:
        """Insere uma nova mensagem de chat"""
        try:
            with obter_conexao() as conexao:
                conexao.execute(
                    chat_sql.INSERIR_CHAT,
                    (chat.id_remetente, chat.id_destinatario, chat.data_hora_envio, chat.mensagem)
                )
                return True
        except Exception as e:
            print(f"Erro ao inserir mensagem de chat: {e}")
            return False

    def obter_mensagens_por_usuario(self, id_usuario: int, pagina: int, tamanho: int) -> List[Chat]:
        """Obtém mensagens de chat de um usuário com paginação"""
        try:
            offset = (pagina - 1) * tamanho
            with obter_conexao() as conexao:
                cursor = conexao.execute(chat_sql.OBTER_MENSAGENS_POR_USUARIO, (id_usuario, id_usuario, tamanho, offset))
                resultados = cursor.fetchall()
                return [Chat(
                    id_remetente=r["id_remetente"],
                    id_destinatario=r["id_destinatario"],
                    mensagem=r["mensagem"],
                    data_hora_envio=r["data_hora_envio"],
                    data_hora_leitura=r["data_hora_leitura"]
                ) for r in resultados]
        except Exception as e:
            print(f"Erro ao obter mensagens por usuário: {e}")
            return []

    def atualizar_data_leitura(self, id_remetente: int, id_destinatario: int, data_envio: datetime, data_leitura: datetime) -> bool:
        """Atualiza a data de leitura de uma mensagem"""
        try:
            with obter_conexao() as conexao:
                cursor = conexao.execute(
                    chat_sql.ATUALIZAR_DATA_LEITURA,
                    (data_leitura, id_remetente, id_destinatario, data_envio)
                )
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar data de leitura: {e}")
            return False

# Instância singleton do repositório
chat_repo = ChatRepo()