from datetime import datetime
from model.chat_model import Chat
from repo import chat_repo, usuario_repo

class TestChatRepo:
    def test_criar_tabela_chat(self, test_db):
        assert chat_repo.criar_tabela_chat() is True

    def test_inserir_chat(self, test_db, chat_exemplo, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:2]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        # Act
        sucesso = chat_repo.inserir_chat(chat_exemplo)
        # Assert
        assert sucesso is True

    def test_obter_mensagens_por_usuario(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:3]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        
        # Inserir algumas mensagens
        chat1 = Chat(1, 2, datetime.now(), "Olá!", None)
        chat2 = Chat(2, 1, datetime.now(), "Oi!", None)
        chat3 = Chat(1, 3, datetime.now(), "Tudo bem?", None)
        
        chat_repo.inserir_chat(chat1)
        chat_repo.inserir_chat(chat2)
        chat_repo.inserir_chat(chat3)
        
        # Act
        mensagens = chat_repo.obter_mensagens_por_usuario(1, 1, 10)
        
        # Assert
        assert len(mensagens) == 3
        assert all(isinstance(m, Chat) for m in mensagens)

    def test_atualizar_data_leitura(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:2]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        
        data_envio = datetime.now()
        chat = Chat(1, 2, data_envio, "Mensagem teste", None)
        chat_repo.inserir_chat(chat)
        
        # Act
        data_leitura = datetime.now()
        sucesso = chat_repo.atualizar_data_leitura(1, 2, data_envio, data_leitura)
        
        # Assert
        assert sucesso is True

    def test_obter_mensagens_paginacao(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo[:3]:
            usuario_repo.inserir_usuario(usuario)
        chat_repo.criar_tabela_chat()
        
        # Inserir 10 mensagens
        for i in range(10):
            chat = Chat(1, 2, datetime.now(), f"Mensagem {i}", None)
            chat_repo.inserir_chat(chat)
        
        # Act
        pagina1 = chat_repo.obter_mensagens_por_usuario(1, 1, 5)
        pagina2 = chat_repo.obter_mensagens_por_usuario(1, 2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 5