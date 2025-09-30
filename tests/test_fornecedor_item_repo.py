import pytest
from core.models.fornecedor_item_model import FornecedorItem
from core.repositories import fornecedor_item_repo, usuario_repo, item_repo

class TestFornecedorItemRepo:
    def test_criar_tabela_fornecedor_item(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        item_repo.criar_tabela_item()
        # Act
        resultado = fornecedor_item_repo.criar_tabela_fornecedor_item()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_fornecedor_item(self, test_db, fornecedor_item_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        item_repo.criar_tabela_item()
        fornecedor_item_repo.criar_tabela_fornecedor_item()
        fornecedor_item = fornecedor_item_factory.criar(id_fornecedor=1, id_item=1)
        # Act
        resultado = fornecedor_item_repo.inserir_fornecedor_item(fornecedor_item)
        # Assert
        assert resultado == True, "A inserção deveria retornar True"
        fornecedor_item_db = fornecedor_item_repo.obter_fornecedor_item(
            fornecedor_item.id_fornecedor, fornecedor_item.id_item)
        assert fornecedor_item_db is not None, "O fornecedor_item inserido não deveria ser None"

    def test_obter_fornecedor_item_existente(self, test_db, fornecedor_item_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        item_repo.criar_tabela_item()
        fornecedor_item_repo.criar_tabela_fornecedor_item()
        fornecedor_item = fornecedor_item_factory.criar(id_fornecedor=1, id_item=1)
        fornecedor_item_repo.inserir_fornecedor_item(fornecedor_item)
        # Act
        fornecedor_item_db = fornecedor_item_repo.obter_fornecedor_item(
            fornecedor_item.id_fornecedor, fornecedor_item.id_item)
        # Assert
        assert fornecedor_item_db is not None
        assert fornecedor_item_db.id_fornecedor == fornecedor_item.id_fornecedor
        assert fornecedor_item_db.id_item == fornecedor_item.id_item

    def test_atualizar_fornecedor_item(self, test_db, fornecedor_item_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        item_repo.criar_tabela_item()
        fornecedor_item_repo.criar_tabela_fornecedor_item()
        fornecedor_item = fornecedor_item_factory.criar(id_fornecedor=1, id_item=1)
        fornecedor_item_repo.inserir_fornecedor_item(fornecedor_item)
        fornecedor_item.preco_personalizado = 150.0
        fornecedor_item.disponivel = False
        # Act
        resultado = fornecedor_item_repo.atualizar_fornecedor_item(fornecedor_item)
        # Assert
        assert resultado == True
        fornecedor_item_db = fornecedor_item_repo.obter_fornecedor_item(
            fornecedor_item.id_fornecedor, fornecedor_item.id_item)
        assert fornecedor_item_db.preco_personalizado == 150.0
        assert fornecedor_item_db.disponivel == False

    def test_excluir_fornecedor_item(self, test_db, fornecedor_item_factory):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        item_repo.criar_tabela_item()
        fornecedor_item_repo.criar_tabela_fornecedor_item()
        fornecedor_item = fornecedor_item_factory.criar(id_fornecedor=1, id_item=1)
        fornecedor_item_repo.inserir_fornecedor_item(fornecedor_item)
        # Act
        resultado = fornecedor_item_repo.excluir_fornecedor_item(
            fornecedor_item.id_fornecedor, fornecedor_item.id_item)
        # Assert
        assert resultado == True
        from util.exceptions import RecursoNaoEncontradoError
        with pytest.raises(RecursoNaoEncontradoError):
            fornecedor_item_repo.obter_fornecedor_item(
                fornecedor_item.id_fornecedor, fornecedor_item.id_item)