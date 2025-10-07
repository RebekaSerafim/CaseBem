from typing import List
from datetime import datetime
from core.repositories.base_repo import BaseRepoChaveComposta
from infrastructure.logging import logger
from core.sql import chat_sql
from core.models.chat_model import Chat


class ChatRepo(BaseRepoChaveComposta):
    """Repositório para operações com chat"""

    def __init__(self):
        super().__init__(
            nome_tabela="chat",
            model_class=Chat,
            sql_module=chat_sql,
            campos_chave=["id_remetente", "id_destinatario", "data_hora_envio"],
        )

    def _objeto_para_tupla_insert(self, chat: Chat) -> tuple:
        """Converte objeto Chat em tupla para INSERT"""
        return (
            chat.id_remetente,
            chat.id_destinatario,
            chat.data_hora_envio,
            chat.mensagem,
        )

    def _objeto_para_tupla_update(self, chat: Chat) -> tuple:
        """Converte objeto Chat em tupla para UPDATE"""
        return (
            chat.mensagem,
            chat.data_hora_leitura,
            chat.id_remetente,
            chat.id_destinatario,
            chat.data_hora_envio,
        )

    def _linha_para_objeto(self, linha: dict) -> Chat:
        """Converte linha do banco em objeto Chat"""
        return Chat(
            id_remetente=linha["id_remetente"],
            id_destinatario=linha["id_destinatario"],
            mensagem=linha["mensagem"],
            data_hora_envio=linha["data_hora_envio"],
            data_hora_leitura=self._safe_get(linha, "data_hora_leitura"),
        )

    def obter_mensagens_por_usuario(
        self, id_usuario: int, pagina: int, tamanho: int
    ) -> List[Chat]:
        """Obtém mensagens de chat de um usuário com paginação"""
        offset = (pagina - 1) * tamanho
        resultados = self.executar_consulta(
            chat_sql.OBTER_MENSAGENS_POR_USUARIO,
            (id_usuario, id_usuario, tamanho, offset),
        )
        mensagens = [self._linha_para_objeto(r) for r in resultados]
        logger.info(
            f"Mensagens de chat obtidas", usuario_id=id_usuario, total=len(mensagens)
        )
        return mensagens

    def atualizar_data_leitura(
        self,
        id_remetente: int,
        id_destinatario: int,
        data_envio: datetime,
        data_leitura: datetime,
    ) -> bool:
        """Atualiza a data de leitura de uma mensagem"""
        sucesso = self.executar_comando(
            chat_sql.ATUALIZAR_DATA_LEITURA,
            (data_leitura, id_remetente, id_destinatario, data_envio),
        )
        if sucesso:
            logger.info(
                f"Data de leitura atualizada",
                remetente_id=id_remetente,
                destinatario_id=id_destinatario,
            )
        return sucesso  # type: ignore[no-any-return]


# Instância singleton do repositório
chat_repo = ChatRepo()
