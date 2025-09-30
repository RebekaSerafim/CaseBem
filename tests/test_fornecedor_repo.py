import pytest
from core.models.fornecedor_model import Fornecedor
from core.models.usuario_model import TipoUsuario
from core.repositories.fornecedor_repo import fornecedor_repo
from core.repositories.usuario_repo import usuario_repo
from util.exceptions import RecursoNaoEncontradoError

class TestFornecedorRepo:
    def test_criar_tabela_fornecedor(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        # Act
        resultado = fornecedor_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        # Assert
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor_inserido)
        assert fornecedor_db is not None, "O fornecedor inserido não deveria ser None"
        assert fornecedor_db.id == id_fornecedor_inserido, "O ID do fornecedor inserido deveria ser igual ao retornado"
        assert fornecedor_db.nome == fornecedor_exemplo.nome, "O nome do fornecedor inserido não confere"
        assert fornecedor_db.cpf == fornecedor_exemplo.cpf, "O CPF do fornecedor inserido não confere"
        assert fornecedor_db.email == fornecedor_exemplo.email, "O email do fornecedor inserido não confere"
        assert fornecedor_db.perfil.value == "FORNECEDOR", "O perfil do fornecedor inserido não confere"
        assert fornecedor_db.nome_empresa == fornecedor_exemplo.nome_empresa, "O nome da empresa não confere"

    def test_obter_fornecedor_por_id_existente(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        # Act
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor_inserido)
        # Assert
        assert fornecedor_db is not None, "O fornecedor retornado deveria ser diferente de None"
        assert fornecedor_db.id == id_fornecedor_inserido, "O ID do fornecedor retornado deveria ser igual ao inserido"

    def test_obter_fornecedor_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            fornecedor_repo.obter_por_id(999)

    def test_atualizar_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        fornecedor_exemplo.id = id_fornecedor_inserido
        fornecedor_exemplo.nome_empresa = "Empresa Atualizada"
        fornecedor_exemplo.descricao = "Nova descrição"
        # Act
        resultado = fornecedor_repo.atualizar(fornecedor_exemplo)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor_inserido)
        assert fornecedor_db.nome_empresa == "Empresa Atualizada", "O nome da empresa deveria ter sido atualizado"
        assert fornecedor_db.descricao == "Nova descrição", "A descrição deveria ter sido atualizada"

    def test_excluir_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        # Act
        resultado = fornecedor_repo.excluir(id_fornecedor_inserido)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        with pytest.raises(RecursoNaoEncontradoError):
            fornecedor_repo.obter_por_id(id_fornecedor_inserido)

