import pytest
from model.categoria_model import Categoria
from model.tipo_fornecimento_model import TipoFornecimento
from repo import categoria_repo
from util.exceptions import RecursoNaoEncontradoError

class TestCategoriaRepo:
    def test_criar_tabela_categorias(self, test_db):
        # Arrange
        # Act
        resultado = categoria_repo.criar_tabela_categorias()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        # Assert
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"
        assert categoria_db.tipo_fornecimento == TipoFornecimento.PRODUTO, "O tipo de fornecimento não confere"
        assert categoria_db.descricao == "Descrição da categoria teste", "A descrição não confere"
        assert categoria_db.ativo == True, "A categoria deveria estar ativa"

    def test_obter_categoria_por_id_existente(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        # Act
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria retornada deveria ser diferente de None"
        assert categoria_db.nome == categoria_exemplo.nome, "O nome da categoria não confere"
        assert categoria_db.tipo_fornecimento == categoria_exemplo.tipo_fornecimento, "O tipo não confere"

    def test_obter_categoria_por_id_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError) as exc_info:
            categoria_repo.obter_categoria_por_id(999)

        assert "Categoria não encontrado" in str(exc_info.value)
        assert "999" in str(exc_info.value)

    def test_atualizar_categoria(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        categoria_exemplo.id = id_categoria_inserida
        categoria_exemplo.nome = "Categoria Atualizada"
        categoria_exemplo.tipo_fornecimento = TipoFornecimento.SERVICO
        categoria_exemplo.ativo = False
        # Act
        resultado = categoria_repo.atualizar_categoria(categoria_exemplo)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome não foi atualizado corretamente"
        assert categoria_db.tipo_fornecimento == TipoFornecimento.SERVICO, "O tipo não foi atualizado corretamente"
        assert categoria_db.ativo == False, "O status ativo não foi atualizado corretamente"

    def test_excluir_categoria(self, test_db, categoria_exemplo):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        id_categoria_inserida = categoria_repo.inserir_categoria(categoria_exemplo)
        # Act
        resultado = categoria_repo.excluir_categoria(id_categoria_inserida)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        categoria_db = categoria_repo.obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db is None, "A categoria excluída não deveria ser encontrada"

    def test_obter_categorias_por_tipo(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria_produto = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição produto", True)
        categoria_servico = Categoria(0, "Categoria Serviço", TipoFornecimento.SERVICO, "Descrição serviço", True)
        categoria_repo.inserir_categoria(categoria_produto)
        categoria_repo.inserir_categoria(categoria_servico)
        # Act
        categorias_produto = categoria_repo.obter_categorias_por_tipo(TipoFornecimento.PRODUTO)
        categorias_servico = categoria_repo.obter_categorias_por_tipo(TipoFornecimento.SERVICO)
        # Assert
        assert len(categorias_produto) == 1, "Deveria ter 1 categoria de produto"
        assert len(categorias_servico) == 1, "Deveria ter 1 categoria de serviço"
        assert categorias_produto[0].tipo_fornecimento == TipoFornecimento.PRODUTO
        assert categorias_servico[0].tipo_fornecimento == TipoFornecimento.SERVICO

    def test_obter_todas_categorias(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria1 = Categoria(0, "Categoria 1", TipoFornecimento.PRODUTO, "Descrição 1", True)
        categoria2 = Categoria(0, "Categoria 2", TipoFornecimento.SERVICO, "Descrição 2", False)
        categoria_repo.inserir_categoria(categoria1)
        categoria_repo.inserir_categoria(categoria2)
        # Act
        todas_categorias = categoria_repo.obter_categorias()
        # Assert
        assert len(todas_categorias) == 2, "Deveria ter 2 categorias no total"

    def test_obter_categorias_ativas(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria_ativa = Categoria(0, "Categoria Ativa", TipoFornecimento.PRODUTO, "Descrição ativa", True)
        categoria_inativa = Categoria(0, "Categoria Inativa", TipoFornecimento.SERVICO, "Descrição inativa", False)
        categoria_repo.inserir_categoria(categoria_ativa)
        categoria_repo.inserir_categoria(categoria_inativa)
        # Act
        categorias_ativas = categoria_repo.obter_categorias_ativas()
        # Assert
        assert len(categorias_ativas) == 1, "Deveria ter apenas 1 categoria ativa"
        assert categorias_ativas[0].ativo == True, "A categoria retornada deveria estar ativa"

    def test_obter_categorias_por_tipo_ativas(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria_produto_ativa = Categoria(0, "Produto Ativo", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_produto_inativa = Categoria(0, "Produto Inativo", TipoFornecimento.PRODUTO, "Descrição", False)
        categoria_servico_ativa = Categoria(0, "Serviço Ativo", TipoFornecimento.SERVICO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria_produto_ativa)
        categoria_repo.inserir_categoria(categoria_produto_inativa)
        categoria_repo.inserir_categoria(categoria_servico_ativa)
        # Act
        categorias_produto_ativas = categoria_repo.obter_categorias_por_tipo_ativas(TipoFornecimento.PRODUTO)
        categorias_servico_ativas = categoria_repo.obter_categorias_por_tipo_ativas(TipoFornecimento.SERVICO)
        # Assert
        assert len(categorias_produto_ativas) == 1, "Deveria ter 1 categoria de produto ativa"
        assert len(categorias_servico_ativas) == 1, "Deveria ter 1 categoria de serviço ativa"
        assert categorias_produto_ativas[0].ativo == True
        assert categorias_servico_ativas[0].ativo == True

    def test_obter_categoria_por_nome_existente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)
        # Act
        categoria_encontrada = categoria_repo.obter_categoria_por_nome("Categoria Teste", TipoFornecimento.PRODUTO)
        # Assert
        assert categoria_encontrada is not None, "Categoria deveria ser encontrada"
        assert categoria_encontrada.nome == "Categoria Teste"
        assert categoria_encontrada.tipo_fornecimento == TipoFornecimento.PRODUTO

    def test_obter_categoria_por_nome_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        categoria_encontrada = categoria_repo.obter_categoria_por_nome("Categoria Inexistente", TipoFornecimento.PRODUTO)
        # Assert
        assert categoria_encontrada is None, "Categoria não deveria ser encontrada"

    def test_obter_categoria_por_nome_tipo_diferente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)
        # Act
        categoria_encontrada = categoria_repo.obter_categoria_por_nome("Categoria Teste", TipoFornecimento.SERVICO)
        # Assert
        assert categoria_encontrada is None, "Categoria não deveria ser encontrada para tipo diferente"

    def test_buscar_categorias_sem_filtros(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria1 = Categoria(0, "Categoria 1", TipoFornecimento.PRODUTO, "Descrição 1", True)
        categoria2 = Categoria(0, "Categoria 2", TipoFornecimento.SERVICO, "Descrição 2", False)
        categoria_repo.inserir_categoria(categoria1)
        categoria_repo.inserir_categoria(categoria2)
        # Act
        categorias = categoria_repo.buscar_categorias()
        # Assert
        assert len(categorias) == 2, "Deveria retornar todas as categorias"

    def test_buscar_categorias_por_nome(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria1 = Categoria(0, "Festa de Casamento", TipoFornecimento.PRODUTO, "Descrição 1", True)
        categoria2 = Categoria(0, "Decoração", TipoFornecimento.SERVICO, "Descrição 2", True)
        categoria_repo.inserir_categoria(categoria1)
        categoria_repo.inserir_categoria(categoria2)
        # Act
        categorias = categoria_repo.buscar_categorias(busca="Festa")
        # Assert
        assert len(categorias) == 1, "Deveria encontrar 1 categoria"
        assert categorias[0].nome == "Festa de Casamento"

    def test_buscar_categorias_por_tipo(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria1 = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição 1", True)
        categoria2 = Categoria(0, "Categoria Serviço", TipoFornecimento.SERVICO, "Descrição 2", True)
        categoria_repo.inserir_categoria(categoria1)
        categoria_repo.inserir_categoria(categoria2)
        # Act
        categorias = categoria_repo.buscar_categorias(tipo_fornecimento="PRODUTO")
        # Assert
        assert len(categorias) == 1, "Deveria encontrar 1 categoria de produto"
        assert categorias[0].tipo_fornecimento == TipoFornecimento.PRODUTO

    def test_buscar_categorias_por_status(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria_ativa = Categoria(0, "Categoria Ativa", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_inativa = Categoria(0, "Categoria Inativa", TipoFornecimento.SERVICO, "Descrição", False)
        categoria_repo.inserir_categoria(categoria_ativa)
        categoria_repo.inserir_categoria(categoria_inativa)
        # Act
        categorias_ativas = categoria_repo.buscar_categorias(status="ativo")
        categorias_inativas = categoria_repo.buscar_categorias(status="inativo")
        # Assert
        assert len(categorias_ativas) == 1, "Deveria encontrar 1 categoria ativa"
        assert len(categorias_inativas) == 1, "Deveria encontrar 1 categoria inativa"
        assert categorias_ativas[0].ativo == True
        assert categorias_inativas[0].ativo == False

    def test_ativar_categoria(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", False)
        id_categoria = categoria_repo.inserir_categoria(categoria)
        # Act
        resultado = categoria_repo.ativar_categoria(id_categoria)
        # Assert
        assert resultado == True, "Ativação deveria retornar True"
        categoria_ativada = categoria_repo.obter_categoria_por_id(id_categoria)
        assert categoria_ativada.ativo == True, "Categoria deveria estar ativa"

    def test_desativar_categoria(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir_categoria(categoria)
        # Act
        resultado = categoria_repo.desativar_categoria(id_categoria)
        # Assert
        assert resultado == True, "Desativação deveria retornar True"
        categoria_desativada = categoria_repo.obter_categoria_por_id(id_categoria)
        assert categoria_desativada.ativo == False, "Categoria deveria estar inativa"

    def test_ativar_categoria_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        resultado = categoria_repo.ativar_categoria(999)
        # Assert
        assert resultado == False, "Ativação de categoria inexistente deveria retornar False"

    def test_desativar_categoria_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela_categorias()
        # Act
        resultado = categoria_repo.desativar_categoria(999)
        # Assert
        assert resultado == False, "Desativação de categoria inexistente deveria retornar False"

@pytest.fixture
def categoria_exemplo():
    return Categoria(
        id=0,
        nome="Categoria Teste",
        tipo_fornecimento=TipoFornecimento.PRODUTO,
        descricao="Descrição da categoria teste",
        ativo=True
    )