"""
Serviço de chat - Lógica de negócio centralizada
"""

from typing import List
from datetime import datetime
from util.exceptions import RegraDeNegocioError
from core.models.chat_model import Chat
from util.logger import logger


class ChatService:
    """Serviço para operações de negócio com chat"""

    def __init__(self):
        from core.repositories import chat_repo, usuario_repo

        self.repo = chat_repo
        self.usuario_repo = usuario_repo

    def enviar_mensagem(self, dados: dict) -> bool:
        """Envia uma mensagem"""
        # Validar que remetente e destinatário existem
        self.usuario_repo.obter_usuario_por_id(dados['id_remetente'])
        self.usuario_repo.obter_usuario_por_id(dados['id_destinatario'])

        # Validar que não está enviando para si mesmo
        if dados['id_remetente'] == dados['id_destinatario']:
            raise RegraDeNegocioError("Não é possível enviar mensagem para si mesmo")

        # Validar mensagem não vazia
        if not dados.get('mensagem') or not dados['mensagem'].strip():
            raise RegraDeNegocioError("Mensagem não pode ser vazia")

        chat = Chat(**dados)
        sucesso = self.repo.inserir_chat(chat)

        if sucesso:
            logger.info(f"Mensagem enviada de {dados['id_remetente']} para {dados['id_destinatario']}")

        return sucesso

    def obter_mensagens(self, id_usuario: int, pagina: int = 1, tamanho: int = 50) -> List[Chat]:
        """Obtém mensagens de um usuário"""
        return self.repo.obter_mensagens_por_usuario(id_usuario, pagina, tamanho)

    def marcar_como_lida(self, id_remetente: int, id_destinatario: int, data_envio: datetime) -> bool:
        """Marca uma mensagem como lida"""
        data_leitura = datetime.now()
        sucesso = self.repo.atualizar_data_leitura(id_remetente, id_destinatario, data_envio, data_leitura)

        if sucesso:
            logger.info(f"Mensagem marcada como lida")

        return sucesso


chat_service = ChatService()