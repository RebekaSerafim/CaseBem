from model.fornecedor_model import Fornecedor
from model.usuario_model import TipoUsuario
from repo import fornecedor_repo, usuario_repo

class TestFornecedorRepo:
    def test_criar_tabela_fornecedor(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        resultado = fornecedor_repo.criar_tabela_fornecedor()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        fornecedor_repo.criar_tabela_fornecedor()
        # Act
        id_fornecedor_inserido = fornecedor_repo.inserir_fornecedor(fornecedor_exemplo)
        # Assert
        fornecedor_db = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor_inserido)
        assert fornecedor_db is not None, "O fornecedor inserido não deveria ser None"
        assert fornecedor_db.id == 1, "O fornecedor inserido deveria ter um ID igual a 1"
        assert fornecedor_db.nome == "Fornecedor Teste", "O nome do fornecedor inserido não confere"
        assert fornecedor_db.cpf == "111.222.333-44", "O CPF do fornecedor inserido não confere"
        assert fornecedor_db.email == "fornecedor@email.com", "O email do fornecedor inserido não confere"
        assert fornecedor_db.perfil.value == "FORNECEDOR", "O perfil do fornecedor inserido não confere"
        assert fornecedor_db.nome_empresa == "Empresa Teste", "O nome da empresa não confere"

    def test_obter_fornecedor_por_id_existente(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        fornecedor_repo.criar_tabela_fornecedor()
        id_fornecedor_inserido = fornecedor_repo.inserir_fornecedor(fornecedor_exemplo)
        # Act
        fornecedor_db = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor_inserido)
        # Assert
        assert fornecedor_db is not None, "O fornecedor retornado deveria ser diferente de None"
        assert fornecedor_db.id == id_fornecedor_inserido, "O ID do fornecedor retornado deveria ser igual ao inserido"

    def test_obter_fornecedor_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        fornecedor_repo.criar_tabela_fornecedor()
        # Act
        fornecedor_db = fornecedor_repo.obter_fornecedor_por_id(999)
        # Assert
        assert fornecedor_db is None, "O fornecedor retornado deveria ser None para ID inexistente"

    def test_atualizar_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        fornecedor_repo.criar_tabela_fornecedor()
        id_fornecedor_inserido = fornecedor_repo.inserir_fornecedor(fornecedor_exemplo)
        fornecedor_exemplo.id = id_fornecedor_inserido
        fornecedor_exemplo.nome_empresa = "Empresa Atualizada"
        fornecedor_exemplo.descricao = "Nova descrição"
        # Act
        resultado = fornecedor_repo.atualizar_fornecedor(fornecedor_exemplo)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        fornecedor_db = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor_inserido)
        assert fornecedor_db.nome_empresa == "Empresa Atualizada", "O nome da empresa deveria ter sido atualizado"
        assert fornecedor_db.descricao == "Nova descrição", "A descrição deveria ter sido atualizada"

    def test_excluir_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        fornecedor_repo.criar_tabela_fornecedor()
        id_fornecedor_inserido = fornecedor_repo.inserir_fornecedor(fornecedor_exemplo)
        # Act
        resultado = fornecedor_repo.excluir_fornecedor(id_fornecedor_inserido)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        fornecedor_db = fornecedor_repo.obter_fornecedor_por_id(id_fornecedor_inserido)
        assert fornecedor_db is None, "O fornecedor deveria ter sido excluído"

