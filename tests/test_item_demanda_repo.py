import pytest
from core.models.item_demanda_model import ItemDemanda
from core.repositories import item_demanda_repo, demanda_repo, item_repo

class TestItemDemandaRepo:
    def test_criar_tabela_item_demanda(self, test_db):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        # Act
        resultado = item_demanda_repo.criar_tabela_item_demanda()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item_demanda(self, test_db, item_demanda_factory):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda = item_demanda_factory.criar(id_demanda=1, id_item=1)
        # Act
        resultado = item_demanda_repo.inserir_item_demanda(item_demanda)
        # Assert
        assert resultado == True, "A inserção deveria retornar True"
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda.id_demanda, item_demanda.id_item)
        assert item_demanda_db is not None, "O item_demanda inserido não deveria ser None"

    def test_obter_item_demanda_existente(self, test_db, item_demanda_factory):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda = item_demanda_factory.criar(id_demanda=1, id_item=1, quantidade=2)
        item_demanda_repo.inserir_item_demanda(item_demanda)
        # Act
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda.id_demanda, item_demanda.id_item)
        # Assert
        assert item_demanda_db is not None
        assert item_demanda_db.id_demanda == item_demanda.id_demanda
        assert item_demanda_db.id_item == item_demanda.id_item
        assert item_demanda_db.quantidade == item_demanda.quantidade

    def test_atualizar_item_demanda(self, test_db, item_demanda_factory):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda = item_demanda_factory.criar(id_demanda=1, id_item=1)
        item_demanda_repo.inserir_item_demanda(item_demanda)
        item_demanda.quantidade = 5
        item_demanda.preco_maximo = 200.0
        # Act
        resultado = item_demanda_repo.atualizar_item_demanda(item_demanda)
        # Assert
        assert resultado == True
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda.id_demanda, item_demanda.id_item)
        assert item_demanda_db.quantidade == 5
        assert item_demanda_db.preco_maximo == 200.0

    def test_excluir_item_demanda(self, test_db, item_demanda_factory):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda = item_demanda_factory.criar(id_demanda=1, id_item=1)
        item_demanda_repo.inserir_item_demanda(item_demanda)
        # Act
        resultado = item_demanda_repo.excluir_item_demanda(
            item_demanda.id_demanda, item_demanda.id_item)
        # Assert
        assert resultado == True
        from util.exceptions import RecursoNaoEncontradoError
        with pytest.raises(RecursoNaoEncontradoError):
            item_demanda_repo.obter_item_demanda(
                item_demanda.id_demanda, item_demanda.id_item)