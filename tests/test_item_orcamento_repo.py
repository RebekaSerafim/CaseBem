import pytest
from model.item_orcamento_model import ItemOrcamento
from repo import item_orcamento_repo, orcamento_repo, item_repo

class TestItemOrcamentoRepo:
    def test_criar_tabela_item_orcamento(self, test_db):
        # Arrange
        orcamento_repo.criar_tabela_orcamento()
        item_repo.criar_tabela_item()
        # Act
        resultado = item_orcamento_repo.criar_tabela_item_orcamento()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item_orcamento(self, test_db, item_orcamento_exemplo):
        # Arrange
        orcamento_repo.criar_tabela_orcamento()
        item_repo.criar_tabela_item()
        item_orcamento_repo.criar_tabela_item_orcamento()
        # Act
        resultado = item_orcamento_repo.inserir_item_orcamento(item_orcamento_exemplo)
        # Assert
        assert resultado == True, "A inserção deveria retornar True"
        item_orcamento_db = item_orcamento_repo.obter_item_orcamento(
            item_orcamento_exemplo.id_orcamento, item_orcamento_exemplo.id_item)
        assert item_orcamento_db is not None, "O item_orcamento inserido não deveria ser None"

    def test_obter_item_orcamento_existente(self, test_db, item_orcamento_exemplo):
        # Arrange
        orcamento_repo.criar_tabela_orcamento()
        item_repo.criar_tabela_item()
        item_orcamento_repo.criar_tabela_item_orcamento()
        item_orcamento_repo.inserir_item_orcamento(item_orcamento_exemplo)
        # Act
        item_orcamento_db = item_orcamento_repo.obter_item_orcamento(
            item_orcamento_exemplo.id_orcamento, item_orcamento_exemplo.id_item)
        # Assert
        assert item_orcamento_db is not None
        assert item_orcamento_db.id_orcamento == item_orcamento_exemplo.id_orcamento
        assert item_orcamento_db.id_item == item_orcamento_exemplo.id_item
        assert item_orcamento_db.quantidade == item_orcamento_exemplo.quantidade
        assert item_orcamento_db.preco_unitario == item_orcamento_exemplo.preco_unitario

    def test_preco_total_property(self, item_orcamento_exemplo):
        # Arrange
        item_orcamento_exemplo.quantidade = 2
        item_orcamento_exemplo.preco_unitario = 50.0
        item_orcamento_exemplo.desconto = 10.0
        # Act
        preco_total = item_orcamento_exemplo.preco_total
        # Assert
        assert preco_total == 90.0, "Preço total deveria ser 2 * 50 - 10 = 90"

    def test_atualizar_item_orcamento(self, test_db, item_orcamento_exemplo):
        # Arrange
        orcamento_repo.criar_tabela_orcamento()
        item_repo.criar_tabela_item()
        item_orcamento_repo.criar_tabela_item_orcamento()
        item_orcamento_repo.inserir_item_orcamento(item_orcamento_exemplo)
        item_orcamento_exemplo.quantidade = 3
        item_orcamento_exemplo.preco_unitario = 75.0
        item_orcamento_exemplo.desconto = 5.0
        # Act
        resultado = item_orcamento_repo.atualizar_item_orcamento(item_orcamento_exemplo)
        # Assert
        assert resultado == True
        item_orcamento_db = item_orcamento_repo.obter_item_orcamento(
            item_orcamento_exemplo.id_orcamento, item_orcamento_exemplo.id_item)
        assert item_orcamento_db.quantidade == 3
        assert item_orcamento_db.preco_unitario == 75.0
        assert item_orcamento_db.desconto == 5.0

    def test_excluir_item_orcamento(self, test_db, item_orcamento_exemplo):
        # Arrange
        orcamento_repo.criar_tabela_orcamento()
        item_repo.criar_tabela_item()
        item_orcamento_repo.criar_tabela_item_orcamento()
        item_orcamento_repo.inserir_item_orcamento(item_orcamento_exemplo)
        # Act
        resultado = item_orcamento_repo.excluir_item_orcamento(
            item_orcamento_exemplo.id_orcamento, item_orcamento_exemplo.id_item)
        # Assert
        assert resultado == True
        import pytest
        from util.exceptions import RecursoNaoEncontradoError
        with pytest.raises(RecursoNaoEncontradoError):
            item_orcamento_repo.obter_item_orcamento(
                item_orcamento_exemplo.id_orcamento, item_orcamento_exemplo.id_item)

@pytest.fixture
def item_orcamento_exemplo():
    return ItemOrcamento(
        id_orcamento=1,
        id_item=1,
        quantidade=2,
        preco_unitario=50.0,
        observacoes="Observações de teste",
        desconto=0.0
    )