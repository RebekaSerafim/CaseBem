from model.noivo_model import Noivo
from repo import noivo_repo

class TestNoivoRepo:
    def test_criar_tabela_noivos(self, test_db):
        assert noivo_repo.criar_tabela_noivos() is True

    def test_inserir_noivo(self, test_db, noivo_exemplo):
        noivo_repo.criar_tabela_noivos()
        id_inserido = noivo_repo.inserir_noivo(noivo_exemplo)
        noivo = noivo_repo.obter_noivo_por_id(id_inserido)
        assert noivo.id == id_inserido

    def test_obter_noivo_por_id_inexistente(self, test_db):
        noivo_repo.criar_tabela_noivos()
        assert noivo_repo.obter_noivo_por_id(999) is None

    def test_atualizar_noivo_existente(self, test_db, noivo_exemplo):
        noivo_repo.criar_tabela_noivos()
        id_inserido = noivo_repo.inserir_noivo(noivo_exemplo)
        noivo = noivo_repo.obter_noivo_por_id(id_inserido)
        noivo.orcamento = 9999.0
        assert noivo_repo.atualizar_noivo(noivo) is True

    def test_atualizar_noivo_inexistente(self, test_db, noivo_exemplo):
        noivo_exemplo.id = 999
        assert noivo_repo.atualizar_noivo(noivo_exemplo) is False

    def test_excluir_noivo_existente(self, test_db, noivo_exemplo):
        noivo_repo.criar_tabela_noivos()
        id_inserido = noivo_repo.inserir_noivo(noivo_exemplo)
        assert noivo_repo.excluir_noivo(id_inserido) is True

    def test_excluir_noivo_inexistente(self, test_db):
        noivo_repo.criar_tabela_noivos()
        assert noivo_repo.excluir_noivo(999) is False

    def test_obter_noivos_por_pagina(self, test_db, lista_noivos_exemplo):
        noivo_repo.criar_tabela_noivos()
        for n in lista_noivos_exemplo:
            noivo_repo.inserir_noivo(n)
        pagina = noivo_repo.obter_noivos_por_pagina(1, 2)
        assert all(isinstance(n, Noivo) for n in pagina)