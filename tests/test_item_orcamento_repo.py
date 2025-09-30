import pytest
from core.models.item_orcamento_model import ItemOrcamento
from core.repositories.item_orcamento_repo import item_orcamento_repo
from core.repositories.orcamento_repo import orcamento_repo
from core.repositories.item_repo import item_repo

class TestItemOrcamentoRepo:
    def test_criar_tabela_item_orcamento(self, test_db):
        # Arrange
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        # Act
        resultado = item_orcamento_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item_orcamento(self, test_db, item_orcamento_factory):
        # Arrange
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        item_orcamento = item_orcamento_factory.criar(id_orcamento=1, id_item=1)
        # Act
        resultado = item_orcamento_repo.inserir(item_orcamento)
        # Assert
        assert resultado == True, "A inserção deveria retornar True"
        item_orcamento_db = item_orcamento_repo.obter(
            item_orcamento.id_orcamento, item_orcamento.id_item)
        assert item_orcamento_db is not None, "O item_orcamento inserido não deveria ser None"

    def test_obter_item_orcamento_existente(self, test_db, item_orcamento_factory):
        # Arrange
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        item_orcamento = item_orcamento_factory.criar(id_orcamento=1, id_item=1, quantidade=2, preco_unitario=50.0)
        item_orcamento_repo.inserir(item_orcamento)
        # Act
        item_orcamento_db = item_orcamento_repo.obter(
            item_orcamento.id_orcamento, item_orcamento.id_item)
        # Assert
        assert item_orcamento_db is not None
        assert item_orcamento_db.id_orcamento == item_orcamento.id_orcamento
        assert item_orcamento_db.id_item == item_orcamento.id_item
        assert item_orcamento_db.quantidade == item_orcamento.quantidade
        assert item_orcamento_db.preco_unitario == item_orcamento.preco_unitario

    def test_preco_total_property(self, item_orcamento_factory):
        # Arrange
        item_orcamento = item_orcamento_factory.criar(quantidade=2, preco_unitario=50.0, desconto=10.0)
        # Act
        preco_total = item_orcamento.preco_total
        # Assert
        assert preco_total == 90.0, "Preço total deveria ser 2 * 50 - 10 = 90"

    def test_atualizar_item_orcamento(self, test_db, item_orcamento_factory):
        # Arrange
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        item_orcamento = item_orcamento_factory.criar(id_orcamento=1, id_item=1)
        item_orcamento_repo.inserir(item_orcamento)
        item_orcamento.quantidade = 3
        item_orcamento.preco_unitario = 75.0
        item_orcamento.desconto = 5.0
        # Act
        resultado = item_orcamento_repo.atualizar(item_orcamento)
        # Assert
        assert resultado == True
        item_orcamento_db = item_orcamento_repo.obter(
            item_orcamento.id_orcamento, item_orcamento.id_item)
        assert item_orcamento_db.quantidade == 3
        assert item_orcamento_db.preco_unitario == 75.0
        assert item_orcamento_db.desconto == 5.0

    def test_excluir_item_orcamento(self, test_db, item_orcamento_factory):
        # Arrange
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        item_orcamento = item_orcamento_factory.criar(id_orcamento=1, id_item=1)
        item_orcamento_repo.inserir(item_orcamento)
        # Act
        resultado = item_orcamento_repo.excluir(
            item_orcamento.id_orcamento, item_orcamento.id_item)
        # Assert
        assert resultado == True
        from util.exceptions import RecursoNaoEncontradoError
        with pytest.raises(RecursoNaoEncontradoError):
            item_orcamento_repo.obter(
                item_orcamento.id_orcamento, item_orcamento.id_item)