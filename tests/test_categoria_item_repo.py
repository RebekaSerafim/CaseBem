import pytest
from model.categoria_item_model import CategoriaItem
from model.item_model import TipoItem
from repo import categoria_item_repo

class TestCategoriaItemRepo:
    def test_criar_tabela_categoria_item(self, test_db):
        # Arrange
        # Act
        resultado = categoria_item_repo.criar_tabela_categoria_item()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria_item(self, test_db, categoria_exemplo):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        # Act
        id_categoria_inserida = categoria_item_repo.inserir_categoria_item(categoria_exemplo)
        # Assert
        categoria_db = categoria_item_repo.obter_categoria_item_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"
        assert categoria_db.tipo_fornecimento == TipoItem.PRODUTO, "O tipo de fornecimento não confere"
        assert categoria_db.descricao == "Descrição da categoria teste", "A descrição não confere"
        assert categoria_db.ativo == True, "A categoria deveria estar ativa"

    def test_obter_categoria_item_por_id_existente(self, test_db, categoria_exemplo):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        id_categoria_inserida = categoria_item_repo.inserir_categoria_item(categoria_exemplo)
        # Act
        categoria_db = categoria_item_repo.obter_categoria_item_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria retornada deveria ser diferente de None"
        assert categoria_db.nome == categoria_exemplo.nome, "O nome da categoria não confere"
        assert categoria_db.tipo_fornecimento == categoria_exemplo.tipo_fornecimento, "O tipo não confere"

    def test_obter_categoria_item_por_id_inexistente(self, test_db):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        # Act
        categoria_db = categoria_item_repo.obter_categoria_item_por_id(999)
        # Assert
        assert categoria_db is None, "A categoria retornada deveria ser None para ID inexistente"

    def test_atualizar_categoria_item(self, test_db, categoria_exemplo):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        id_categoria_inserida = categoria_item_repo.inserir_categoria_item(categoria_exemplo)
        categoria_exemplo.id = id_categoria_inserida
        categoria_exemplo.nome = "Categoria Atualizada"
        categoria_exemplo.tipo_fornecimento = TipoItem.SERVICO
        categoria_exemplo.ativo = False
        # Act
        resultado = categoria_item_repo.atualizar_categoria_item(categoria_exemplo)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        categoria_db = categoria_item_repo.obter_categoria_item_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome não foi atualizado corretamente"
        assert categoria_db.tipo_fornecimento == TipoItem.SERVICO, "O tipo não foi atualizado corretamente"
        assert categoria_db.ativo == False, "O status ativo não foi atualizado corretamente"

    def test_excluir_categoria_item(self, test_db, categoria_exemplo):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        id_categoria_inserida = categoria_item_repo.inserir_categoria_item(categoria_exemplo)
        # Act
        resultado = categoria_item_repo.excluir_categoria_item(id_categoria_inserida)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        categoria_db = categoria_item_repo.obter_categoria_item_por_id(id_categoria_inserida)
        assert categoria_db is None, "A categoria excluída não deveria ser encontrada"

    def test_obter_categorias_por_tipo(self, test_db):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        categoria_produto = CategoriaItem(0, "Categoria Produto", TipoItem.PRODUTO, "Descrição produto", True)
        categoria_servico = CategoriaItem(0, "Categoria Serviço", TipoItem.SERVICO, "Descrição serviço", True)
        categoria_item_repo.inserir_categoria_item(categoria_produto)
        categoria_item_repo.inserir_categoria_item(categoria_servico)
        # Act
        categorias_produto = categoria_item_repo.obter_categorias_por_tipo(TipoItem.PRODUTO)
        categorias_servico = categoria_item_repo.obter_categorias_por_tipo(TipoItem.SERVICO)
        # Assert
        assert len(categorias_produto) == 1, "Deveria ter 1 categoria de produto"
        assert len(categorias_servico) == 1, "Deveria ter 1 categoria de serviço"
        assert categorias_produto[0].tipo_fornecimento == TipoItem.PRODUTO
        assert categorias_servico[0].tipo_fornecimento == TipoItem.SERVICO

    def test_obter_todas_categorias(self, test_db):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        categoria1 = CategoriaItem(0, "Categoria 1", TipoItem.PRODUTO, "Descrição 1", True)
        categoria2 = CategoriaItem(0, "Categoria 2", TipoItem.SERVICO, "Descrição 2", False)
        categoria_item_repo.inserir_categoria_item(categoria1)
        categoria_item_repo.inserir_categoria_item(categoria2)
        # Act
        todas_categorias = categoria_item_repo.obter_todas_categorias()
        # Assert
        assert len(todas_categorias) == 2, "Deveria ter 2 categorias no total"

    def test_obter_categorias_ativas(self, test_db):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        categoria_ativa = CategoriaItem(0, "Categoria Ativa", TipoItem.PRODUTO, "Descrição ativa", True)
        categoria_inativa = CategoriaItem(0, "Categoria Inativa", TipoItem.SERVICO, "Descrição inativa", False)
        categoria_item_repo.inserir_categoria_item(categoria_ativa)
        categoria_item_repo.inserir_categoria_item(categoria_inativa)
        # Act
        categorias_ativas = categoria_item_repo.obter_categorias_ativas()
        # Assert
        assert len(categorias_ativas) == 1, "Deveria ter apenas 1 categoria ativa"
        assert categorias_ativas[0].ativo == True, "A categoria retornada deveria estar ativa"

    def test_obter_categorias_por_tipo_ativas(self, test_db):
        # Arrange
        categoria_item_repo.criar_tabela_categoria_item()
        categoria_produto_ativa = CategoriaItem(0, "Produto Ativo", TipoItem.PRODUTO, "Descrição", True)
        categoria_produto_inativa = CategoriaItem(0, "Produto Inativo", TipoItem.PRODUTO, "Descrição", False)
        categoria_servico_ativa = CategoriaItem(0, "Serviço Ativo", TipoItem.SERVICO, "Descrição", True)
        categoria_item_repo.inserir_categoria_item(categoria_produto_ativa)
        categoria_item_repo.inserir_categoria_item(categoria_produto_inativa)
        categoria_item_repo.inserir_categoria_item(categoria_servico_ativa)
        # Act
        categorias_produto_ativas = categoria_item_repo.obter_categorias_por_tipo_ativas(TipoItem.PRODUTO)
        categorias_servico_ativas = categoria_item_repo.obter_categorias_por_tipo_ativas(TipoItem.SERVICO)
        # Assert
        assert len(categorias_produto_ativas) == 1, "Deveria ter 1 categoria de produto ativa"
        assert len(categorias_servico_ativas) == 1, "Deveria ter 1 categoria de serviço ativa"
        assert categorias_produto_ativas[0].ativo == True
        assert categorias_servico_ativas[0].ativo == True

@pytest.fixture
def categoria_exemplo():
    return CategoriaItem(
        id=0,
        nome="Categoria Teste",
        tipo_fornecimento=TipoItem.PRODUTO,
        descricao="Descrição da categoria teste",
        ativo=True
    )