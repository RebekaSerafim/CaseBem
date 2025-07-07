
from model.item_contrato_servico_model import ItemContrato
from repo import item_contrato_repo

class TestItemContratoRepo:
    def test_criar_tabela_itens_contrato_servico(self, test_db):
        assert item_contrato_repo.criar_tabela_itens_contrato_servico
() == True

    def test_inserir_item(self, test_db, item_exemplo):
        id_inserido = item_contrato_servico_repo.inserir_item_contrato_servico(item_exemplo)
        item = item_contrato_repo.obter_item_contrato_por_id(id_inserido)
        assert item.id == id_inserido

    def test_obter_item_por_id_inexistente(self, test_db):
        assert item_contrato_repo.obter_item_contrato_por_id(999) is None

    def test_atualizar_item_existente(self, test_db, item_exemplo):
        id_inserido = item_contrato_repo.inserir_item_contrato(item_exemplo)
        item = item_contrato_repo.obter_item_contrato_por_id(id_inserido)
        item.quantidade = 10
        assert item_contrato_repo.atualizar_item_contrato(item) == True

    def test_atualizar_item_inexistente(self, test_db, item_exemplo):
        item_exemplo.id = 999
        assert item_contrato_repo.atualizar_item_contrato(item_exemplo) == False

    def test_excluir_item_existente(self, test_db, item_exemplo):
        id_inserido = item_contrato_repo.inserir_item_contrato(item_exemplo)
        assert item_contrato_repo.excluir_item_contrato(id_inserido) == True

    def test_excluir_item_inexistente(self, test_db):
        assert item_contrato_repo.excluir_item_contrato(999) == False

    def test_obter_itens_por_pagina(self, test_db, lista_itens):
        for i in lista_itens:
            item_contrato_repo.inserir_item_contrato(i)
        pagina = item_contrato_repo.obter_itens_contrato_por_pagina(1, 2)
        assert all(isinstance(i, ItemContrato) for i in pagina)
