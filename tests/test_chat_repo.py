from model.chat_model import Chat
from repo import chat_repo

class TestChatRepo:
    def test_criar_tabela_chat(self, test_db):
        assert chat_repo.criar_tabela_chat() is True

    def test_inserir_mensagem(self, test_db, chat_exemplo):
        chat_repo.criar_tabela_chat()
        id_msg = chat_repo.inserir_mensagem(chat_exemplo)
        msg = chat_repo.obter_mensagem_por_id(id_msg)

        assert msg is not None
        assert msg.idRemetente == chat_exemplo.idRemetente
        assert msg.idDestinatario == chat_exemplo.idDestinatario
        assert msg.Mensagem == chat_exemplo.Mensagem

    def test_obter_mensagem_inexistente(self, test_db):
        chat_repo.criar_tabela_chat()
        msg = chat_repo.obter_mensagem_por_id(999)
        assert msg is None

    def test_excluir_mensagem(self, test_db, chat_exemplo):
        chat_repo.criar_tabela_chat()
        id_msg = chat_repo.inserir_mensagem(chat_exemplo)
        assert chat_repo.excluir_mensagem(id_msg) is True
        assert chat_repo.obter_mensagem_por_id(id_msg) is None