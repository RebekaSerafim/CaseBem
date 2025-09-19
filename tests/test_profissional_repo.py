from model.profissional_model import Profissional
from model.usuario_model import TipoUsuario
from repo import profissional_repo, usuario_repo

class TestProfissionalRepo:
    def test_criar_tabela_profissional(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        # Act
        resultado = profissional_repo.criar_tabela_profissional()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_profissional(self, test_db, profissional_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        # Act
        id_profissional_inserido = profissional_repo.inserir_profissional(profissional_exemplo)
        # Assert
        profissional_db = profissional_repo.obter_profissional_por_id(id_profissional_inserido)
        assert profissional_db is not None, "O profissional inserido não deveria ser None"
        assert profissional_db.id == 1, "O profissional inserido deveria ter um ID igual a 1"
        assert profissional_db.nome == "Profissional Teste", "O nome do profissional inserido não confere"
        assert profissional_db.cpf == "111.222.333-44", "O CPF do profissional inserido não confere"
        assert profissional_db.email == "profissional@email.com", "O email do profissional inserido não confere"
        assert profissional_db.perfil.value == "PROFISSIONAL", "O perfil do profissional inserido não confere"
        assert profissional_db.nome_empresa == "Empresa Teste", "O nome da empresa não confere"
        assert profissional_db.prestador == True, "O profissional deveria ser prestador"
        assert profissional_db.fornecedor == True, "O profissional deveria ser fornecedor"
        assert profissional_db.locador == False, "O profissional não deveria ser locador"

    def test_obter_profissional_por_id_existente(self, test_db, profissional_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        id_profissional_inserido = profissional_repo.inserir_profissional(profissional_exemplo)
        # Act
        profissional_db = profissional_repo.obter_profissional_por_id(id_profissional_inserido)
        # Assert
        assert profissional_db is not None, "O profissional retornado deveria ser diferente de None"
        assert profissional_db.id == id_profissional_inserido, "O ID do profissional retornado deveria ser igual ao inserido"

    def test_obter_profissional_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        # Act
        profissional_db = profissional_repo.obter_profissional_por_id(999)
        # Assert
        assert profissional_db is None, "O profissional retornado deveria ser None para ID inexistente"

    def test_atualizar_profissional(self, test_db, profissional_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        id_profissional_inserido = profissional_repo.inserir_profissional(profissional_exemplo)
        profissional_exemplo.id = id_profissional_inserido
        profissional_exemplo.nome_empresa = "Empresa Atualizada"
        profissional_exemplo.descricao = "Nova descrição"
        # Act
        resultado = profissional_repo.atualizar_profissional(profissional_exemplo)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        profissional_db = profissional_repo.obter_profissional_por_id(id_profissional_inserido)
        assert profissional_db.nome_empresa == "Empresa Atualizada", "O nome da empresa deveria ter sido atualizado"
        assert profissional_db.descricao == "Nova descrição", "A descrição deveria ter sido atualizada"

    def test_excluir_profissional(self, test_db, profissional_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        id_profissional_inserido = profissional_repo.inserir_profissional(profissional_exemplo)
        # Act
        resultado = profissional_repo.excluir_profissional(id_profissional_inserido)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        profissional_db = profissional_repo.obter_profissional_por_id(id_profissional_inserido)
        assert profissional_db is None, "O profissional deveria ter sido excluído"

    def test_obter_prestadores(self, test_db, lista_profissionais_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        for profissional in lista_profissionais_exemplo:
            profissional_repo.inserir_profissional(profissional)
        # Act
        prestadores = profissional_repo.obter_prestadores()
        # Assert
        assert len(prestadores) > 0, "Deveria retornar pelo menos um prestador"
        for prestador in prestadores:
            assert prestador.prestador == True, "Todos os retornados deveriam ser prestadores"

    def test_obter_fornecedores(self, test_db, lista_profissionais_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        for profissional in lista_profissionais_exemplo:
            profissional_repo.inserir_profissional(profissional)
        # Act
        fornecedores = profissional_repo.obter_fornecedores()
        # Assert
        assert len(fornecedores) > 0, "Deveria retornar pelo menos um fornecedor"
        for fornecedor in fornecedores:
            assert fornecedor.fornecedor == True, "Todos os retornados deveriam ser fornecedores"

    def test_obter_locadores(self, test_db, lista_profissionais_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        profissional_repo.criar_tabela_profissional()
        for profissional in lista_profissionais_exemplo:
            profissional_repo.inserir_profissional(profissional)
        # Act
        locadores = profissional_repo.obter_locadores()
        # Assert
        assert len(locadores) > 0, "Deveria retornar pelo menos um locador"
        for locador in locadores:
            assert locador.locador == True, "Todos os retornados deveriam ser locadores"