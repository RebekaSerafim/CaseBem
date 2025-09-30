import pytest
from datetime import datetime
from core.models.chat_model import Chat
from core.repositories import chat_repo, usuario_repo

class TestChatRepo:
    def test_criar_tabela_chat(self, test_db):
        assert chat_repo.criar_tabela_chat() is True

    def test_inserir_chat(self, test_db, chat_factory, usuario_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuarios = usuario_factory.criar_lista(2)
        for usuario in usuarios:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        chat = chat_factory.criar(id_remetente=1, id_destinatario=2, mensagem="Mensagem de teste")
        # Act
        sucesso = chat_repo.inserir_chat(chat)
        # Assert
        assert sucesso is True

    def test_obter_mensagens_por_usuario(self, test_db, usuario_factory, chat_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuarios = usuario_factory.criar_lista(3)
        for usuario in usuarios:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()

        # Inserir algumas mensagens
        chat1 = chat_factory.criar(id_remetente=1, id_destinatario=2, mensagem="Olá!")
        chat2 = chat_factory.criar(id_remetente=2, id_destinatario=1, mensagem="Oi!")
        chat3 = chat_factory.criar(id_remetente=1, id_destinatario=3, mensagem="Tudo bem?")

        chat_repo.inserir_chat(chat1)
        chat_repo.inserir_chat(chat2)
        chat_repo.inserir_chat(chat3)
        
        # Act
        mensagens = chat_repo.obter_mensagens_por_usuario(1, 1, 10)
        
        # Assert
        assert len(mensagens) == 3
        assert all(isinstance(m, Chat) for m in mensagens)

    def test_atualizar_data_leitura(self, test_db, usuario_factory, chat_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuarios = usuario_factory.criar_lista(2)
        for usuario in usuarios:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()

        data_envio = datetime.now()
        chat = chat_factory.criar(id_remetente=1, id_destinatario=2, data_hora_envio=data_envio, mensagem="Mensagem teste")
        chat_repo.inserir_chat(chat)
        
        # Act
        data_leitura = datetime.now()
        sucesso = chat_repo.atualizar_data_leitura(1, 2, data_envio, data_leitura)
        
        # Assert
        assert sucesso is True

    def test_obter_mensagens_paginacao(self, test_db, usuario_factory, chat_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuarios = usuario_factory.criar_lista(3)
        for usuario in usuarios:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()

        # Inserir 10 mensagens
        for i in range(10):
            chat = chat_factory.criar(id_remetente=1, id_destinatario=2, mensagem=f"Mensagem {i}")
            chat_repo.inserir_chat(chat)
        
        # Act
        pagina1 = chat_repo.obter_mensagens_por_usuario(1, 1, 5)
        pagina2 = chat_repo.obter_mensagens_por_usuario(1, 2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 5