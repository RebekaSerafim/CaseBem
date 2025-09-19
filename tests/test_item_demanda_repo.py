import pytest
from model.item_demanda_model import ItemDemanda
from repo import item_demanda_repo, demanda_repo, item_repo

class TestItemDemandaRepo:
    def test_criar_tabela_item_demanda(self, test_db):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        # Act
        resultado = item_demanda_repo.criar_tabela_item_demanda()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item_demanda(self, test_db, item_demanda_exemplo):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        # Act
        resultado = item_demanda_repo.inserir_item_demanda(item_demanda_exemplo)
        # Assert
        assert resultado == True, "A inserção deveria retornar True"
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda_exemplo.id_demanda, item_demanda_exemplo.id_item)
        assert item_demanda_db is not None, "O item_demanda inserido não deveria ser None"

    def test_obter_item_demanda_existente(self, test_db, item_demanda_exemplo):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda_repo.inserir_item_demanda(item_demanda_exemplo)
        # Act
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda_exemplo.id_demanda, item_demanda_exemplo.id_item)
        # Assert
        assert item_demanda_db is not None
        assert item_demanda_db.id_demanda == item_demanda_exemplo.id_demanda
        assert item_demanda_db.id_item == item_demanda_exemplo.id_item
        assert item_demanda_db.quantidade == item_demanda_exemplo.quantidade

    def test_atualizar_item_demanda(self, test_db, item_demanda_exemplo):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda_repo.inserir_item_demanda(item_demanda_exemplo)
        item_demanda_exemplo.quantidade = 5
        item_demanda_exemplo.preco_maximo = 200.0
        # Act
        resultado = item_demanda_repo.atualizar_item_demanda(item_demanda_exemplo)
        # Assert
        assert resultado == True
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda_exemplo.id_demanda, item_demanda_exemplo.id_item)
        assert item_demanda_db.quantidade == 5
        assert item_demanda_db.preco_maximo == 200.0

    def test_excluir_item_demanda(self, test_db, item_demanda_exemplo):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        item_repo.criar_tabela_item()
        item_demanda_repo.criar_tabela_item_demanda()
        item_demanda_repo.inserir_item_demanda(item_demanda_exemplo)
        # Act
        resultado = item_demanda_repo.excluir_item_demanda(
            item_demanda_exemplo.id_demanda, item_demanda_exemplo.id_item)
        # Assert
        assert resultado == True
        item_demanda_db = item_demanda_repo.obter_item_demanda(
            item_demanda_exemplo.id_demanda, item_demanda_exemplo.id_item)
        assert item_demanda_db is None

@pytest.fixture
def item_demanda_exemplo():
    return ItemDemanda(
        id_demanda=1,
        id_item=1,
        quantidade=2,
        observacoes="Observações de teste",
        preco_maximo=100.0
    )