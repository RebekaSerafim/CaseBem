from typing import List
from datetime import datetime
from util.base_repo import BaseRepoChaveComposta
from sql import chat_sql
from model.chat_model import Chat

class ChatRepo(BaseRepoChaveComposta):
    """Repositório para operações com chat (chave composta)"""

    def __init__(self):
        # Chat tem chave composta: (id_remetente, id_destinatario, data_hora_envio)
        super().__init__('chat', Chat, chat_sql, ['id_remetente', 'id_destinatario', 'data_hora_envio'])

    def _objeto_para_tupla_insert(self, chat: Chat) -> tuple:
        """Prepara dados do chat para inserção"""
        return (
            chat.id_remetente,
            chat.id_destinatario,
            chat.data_hora_envio,
            chat.mensagem
        )

    def _objeto_para_tupla_update(self, chat: Chat) -> tuple:
        """Prepara dados do chat para atualização"""
        return (
            chat.mensagem,
            chat.data_hora_leitura,
            chat.id_remetente,
            chat.id_destinatario,
            chat.data_hora_envio
        )

    def _linha_para_objeto(self, linha: dict) -> Chat:
        """Converte linha do banco em objeto Chat"""
        linha_dict = dict(linha) if hasattr(linha, 'keys') else linha

        return Chat(
            id_remetente=linha_dict["id_remetente"],
            id_destinatario=linha_dict["id_destinatario"],
            mensagem=linha_dict["mensagem"],
            data_hora_envio=linha_dict["data_hora_envio"],
            data_hora_leitura=linha_dict.get("data_hora_leitura")
        )

    def obter_mensagens_por_usuario(self, id_usuario: int, pagina: int, tamanho: int) -> List[Chat]:
        """Obtém mensagens de um usuário com paginação"""
        offset = (pagina - 1) * tamanho
        resultados = self.executar_query(chat_sql.OBTER_MENSAGENS_POR_USUARIO, (id_usuario, id_usuario, tamanho, offset))
        return [self._linha_para_objeto(row) for row in resultados]

    def atualizar_data_leitura(self, id_remetente: int, id_destinatario: int, data_envio: datetime, data_leitura: datetime) -> bool:
        """Atualiza data de leitura de uma mensagem específica"""
        return self.executar_comando(chat_sql.ATUALIZAR_DATA_LEITURA, (data_leitura, id_remetente, id_destinatario, data_envio))

# Instância global do repositório
chat_repo = ChatRepo()

# Funções de compatibilidade (para não quebrar código existente)
def criar_tabela_chat() -> bool:
    return chat_repo.criar_tabela()

def inserir_chat(chat: Chat) -> bool:
    return chat_repo.inserir(chat)

def obter_mensagens_por_usuario(id_usuario: int, pagina: int, tamanho: int) -> List[Chat]:
    return chat_repo.obter_mensagens_por_usuario(id_usuario, pagina, tamanho)

def atualizar_data_leitura(id_remetente: int, id_destinatario: int, data_envio: datetime, data_leitura: datetime) -> bool:
    return chat_repo.atualizar_data_leitura(id_remetente, id_destinatario, data_envio, data_leitura)

def obter_chat_por_chave(id_remetente: int, id_destinatario: int, data_envio: datetime) -> Chat:
    return chat_repo.obter_por_chave(id_remetente, id_destinatario, data_envio)

def excluir_chat(id_remetente: int, id_destinatario: int, data_envio: datetime) -> bool:
    return chat_repo.excluir(id_remetente, id_destinatario, data_envio)

def listar_chats() -> List[Chat]:
    return chat_repo.listar_todos()
