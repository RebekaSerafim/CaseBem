import pytest
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories.categoria_repo import categoria_repo
from util.exceptions import RecursoNaoEncontradoError

class TestCategoriaRepo:
    def test_criar_tabela_categorias(self, test_db):
        # Arrange
        # Act
        resultado = categoria_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar(nome="Categoria Teste", tipo_fornecimento=TipoFornecimento.PRODUTO)
        # Act
        id_categoria_inserida = categoria_repo.inserir(categoria)
        # Assert
        categoria_db = categoria_repo.obter_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"
        assert categoria_db.tipo_fornecimento == TipoFornecimento.PRODUTO, "O tipo de fornecimento não confere"
        assert categoria_db.ativo == True, "A categoria deveria estar ativa"

    def test_obter_categoria_por_id_existente(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar()
        id_categoria_inserida = categoria_repo.inserir(categoria)
        # Act
        categoria_db = categoria_repo.obter_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria retornada deveria ser diferente de None"
        assert categoria_db.nome == categoria.nome, "O nome da categoria não confere"
        assert categoria_db.tipo_fornecimento == categoria.tipo_fornecimento, "O tipo não confere"

    def test_obter_categoria_por_id_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError) as exc_info:
            categoria_repo.obter_por_id(999)

        assert "Categoria não encontrado" in str(exc_info.value)
        assert "999" in str(exc_info.value)

    def test_atualizar_categoria(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar()
        id_categoria_inserida = categoria_repo.inserir(categoria)
        categoria.id = id_categoria_inserida
        categoria.nome = "Categoria Atualizada"
        categoria.tipo_fornecimento = TipoFornecimento.SERVICO
        categoria.ativo = False
        # Act
        resultado = categoria_repo.atualizar(categoria)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        categoria_db = categoria_repo.obter_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome não foi atualizado corretamente"
        assert categoria_db.tipo_fornecimento == TipoFornecimento.SERVICO, "O tipo não foi atualizado corretamente"
        assert categoria_db.ativo == False, "O status ativo não foi atualizado corretamente"

    def test_excluir_categoria(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar()
        id_categoria_inserida = categoria_repo.inserir(categoria)
        # Act
        resultado = categoria_repo.excluir(id_categoria_inserida)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        with pytest.raises(RecursoNaoEncontradoError):
            categoria_repo.obter_por_id(id_categoria_inserida)

    def test_obter_categorias_por_tipo(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria_produto = categoria_factory.criar(nome="Categoria Produto", tipo_fornecimento=TipoFornecimento.PRODUTO)
        categoria_servico = categoria_factory.criar(nome="Categoria Serviço", tipo_fornecimento=TipoFornecimento.SERVICO)
        categoria_repo.inserir(categoria_produto)
        categoria_repo.inserir(categoria_servico)
        # Act
        categorias_produto = categoria_repo.obter_por_tipo(TipoFornecimento.PRODUTO)
        categorias_servico = categoria_repo.obter_por_tipo(TipoFornecimento.SERVICO)
        # Assert
        assert len(categorias_produto) == 1, "Deveria ter 1 categoria de produto"
        assert len(categorias_servico) == 1, "Deveria ter 1 categoria de serviço"
        assert categorias_produto[0].tipo_fornecimento == TipoFornecimento.PRODUTO
        assert categorias_servico[0].tipo_fornecimento == TipoFornecimento.SERVICO

    def test_obter_todas_categorias(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria1 = categoria_factory.criar(nome="Categoria 1", tipo_fornecimento=TipoFornecimento.PRODUTO, ativo=True)
        categoria2 = categoria_factory.criar(nome="Categoria 2", tipo_fornecimento=TipoFornecimento.SERVICO, ativo=False)
        categoria_repo.inserir(categoria1)
        categoria_repo.inserir(categoria2)
        # Act
        todas_categorias = categoria_repo.listar_todos()
        # Assert
        assert len(todas_categorias) == 2, "Deveria ter 2 categorias no total"

    def test_obter_categorias_ativas(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria_ativa = categoria_factory.criar(nome="Categoria Ativa", ativo=True)
        categoria_inativa = categoria_factory.criar(nome="Categoria Inativa", ativo=False)
        categoria_repo.inserir(categoria_ativa)
        categoria_repo.inserir(categoria_inativa)
        # Act
        categorias_ativas = categoria_repo.listar_todos(ativo=True)
        # Assert
        assert len(categorias_ativas) == 1, "Deveria ter apenas 1 categoria ativa"
        assert categorias_ativas[0].ativo == True, "A categoria retornada deveria estar ativa"

    def test_obter_categorias_por_tipo_ativas(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria_produto_ativa = categoria_factory.criar(nome="Produto Ativo", tipo_fornecimento=TipoFornecimento.PRODUTO, ativo=True)
        categoria_produto_inativa = categoria_factory.criar(nome="Produto Inativo", tipo_fornecimento=TipoFornecimento.PRODUTO, ativo=False)
        categoria_servico_ativa = categoria_factory.criar(nome="Serviço Ativo", tipo_fornecimento=TipoFornecimento.SERVICO, ativo=True)
        categoria_repo.inserir(categoria_produto_ativa)
        categoria_repo.inserir(categoria_produto_inativa)
        categoria_repo.inserir(categoria_servico_ativa)
        # Act
        categorias_produto_ativas = categoria_repo.obter_por_tipo_ativas(TipoFornecimento.PRODUTO)
        categorias_servico_ativas = categoria_repo.obter_por_tipo_ativas(TipoFornecimento.SERVICO)
        # Assert
        assert len(categorias_produto_ativas) == 1, "Deveria ter 1 categoria de produto ativa"
        assert len(categorias_servico_ativas) == 1, "Deveria ter 1 categoria de serviço ativa"
        assert categorias_produto_ativas[0].ativo == True
        assert categorias_servico_ativas[0].ativo == True

    def test_obter_categoria_por_nome_existente(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar(nome="Categoria Teste", tipo_fornecimento=TipoFornecimento.PRODUTO)
        categoria_repo.inserir(categoria)
        # Act
        categoria_encontrada = categoria_repo.obter_por_nome("Categoria Teste", TipoFornecimento.PRODUTO)
        # Assert
        assert categoria_encontrada is not None, "Categoria deveria ser encontrada"
        assert categoria_encontrada.nome == "Categoria Teste"
        assert categoria_encontrada.tipo_fornecimento == TipoFornecimento.PRODUTO

    def test_obter_categoria_por_nome_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela()
        # Act
        categoria_encontrada = categoria_repo.obter_por_nome("Categoria Inexistente", TipoFornecimento.PRODUTO)
        # Assert
        assert categoria_encontrada is None, "Categoria não deveria ser encontrada"

    def test_obter_categoria_por_nome_tipo_diferente(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar(nome="Categoria Teste", tipo_fornecimento=TipoFornecimento.PRODUTO)
        categoria_repo.inserir(categoria)
        # Act
        categoria_encontrada = categoria_repo.obter_por_nome("Categoria Teste", TipoFornecimento.SERVICO)
        # Assert
        assert categoria_encontrada is None, "Categoria não deveria ser encontrada para tipo diferente"

    def test_buscar_categorias_sem_filtros(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria1 = categoria_factory.criar(nome="Categoria 1", tipo_fornecimento=TipoFornecimento.PRODUTO, ativo=True)
        categoria2 = categoria_factory.criar(nome="Categoria 2", tipo_fornecimento=TipoFornecimento.SERVICO, ativo=False)
        categoria_repo.inserir(categoria1)
        categoria_repo.inserir(categoria2)
        # Act
        categorias = categoria_repo.buscar_categorias()
        # Assert
        assert len(categorias) == 2, "Deveria retornar todas as categorias"

    def test_buscar_categorias_por_nome(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria1 = categoria_factory.criar(nome="Festa de Casamento", tipo_fornecimento=TipoFornecimento.PRODUTO)
        categoria2 = categoria_factory.criar(nome="Decoração", tipo_fornecimento=TipoFornecimento.SERVICO)
        categoria_repo.inserir(categoria1)
        categoria_repo.inserir(categoria2)
        # Act
        categorias = categoria_repo.buscar_categorias(busca="Festa")
        # Assert
        assert len(categorias) == 1, "Deveria encontrar 1 categoria"
        assert categorias[0].nome == "Festa de Casamento"

    def test_buscar_categorias_por_tipo(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria1 = categoria_factory.criar(nome="Categoria Produto", tipo_fornecimento=TipoFornecimento.PRODUTO)
        categoria2 = categoria_factory.criar(nome="Categoria Serviço", tipo_fornecimento=TipoFornecimento.SERVICO)
        categoria_repo.inserir(categoria1)
        categoria_repo.inserir(categoria2)
        # Act
        categorias = categoria_repo.buscar_categorias(tipo_fornecimento="PRODUTO")
        # Assert
        assert len(categorias) == 1, "Deveria encontrar 1 categoria de produto"
        assert categorias[0].tipo_fornecimento == TipoFornecimento.PRODUTO

    def test_buscar_categorias_por_status(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria_ativa = categoria_factory.criar(nome="Categoria Ativa", ativo=True)
        categoria_inativa = categoria_factory.criar(nome="Categoria Inativa", ativo=False)
        categoria_repo.inserir(categoria_ativa)
        categoria_repo.inserir(categoria_inativa)
        # Act
        categorias_ativas = categoria_repo.buscar_categorias(status="ativo")
        categorias_inativas = categoria_repo.buscar_categorias(status="inativo")
        # Assert
        assert len(categorias_ativas) == 1, "Deveria encontrar 1 categoria ativa"
        assert len(categorias_inativas) == 1, "Deveria encontrar 1 categoria inativa"
        assert categorias_ativas[0].ativo == True
        assert categorias_inativas[0].ativo == False

    def test_ativar_categoria(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar(nome="Categoria Teste", ativo=False)
        id_categoria = categoria_repo.inserir(categoria)
        # Act
        resultado = categoria_repo.ativar_categoria(id_categoria)
        # Assert
        assert resultado == True, "Ativação deveria retornar True"
        categoria_ativada = categoria_repo.obter_por_id(id_categoria)
        assert categoria_ativada.ativo == True, "Categoria deveria estar ativa"

    def test_desativar_categoria(self, test_db, categoria_factory):
        # Arrange
        categoria_repo.criar_tabela()
        categoria = categoria_factory.criar(nome="Categoria Teste", ativo=True)
        id_categoria = categoria_repo.inserir(categoria)
        # Act
        resultado = categoria_repo.desativar_categoria(id_categoria)
        # Assert
        assert resultado == True, "Desativação deveria retornar True"
        categoria_desativada = categoria_repo.obter_por_id(id_categoria)
        assert categoria_desativada.ativo == False, "Categoria deveria estar inativa"

    def test_ativar_categoria_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela()
        # Act
        resultado = categoria_repo.ativar_categoria(999)
        # Assert
        assert resultado == False, "Ativação de categoria inexistente deveria retornar False"

    def test_desativar_categoria_inexistente(self, test_db):
        # Arrange
        categoria_repo.criar_tabela()
        # Act
        resultado = categoria_repo.desativar_categoria(999)
        # Assert
        assert resultado == False, "Desativação de categoria inexistente deveria retornar False"