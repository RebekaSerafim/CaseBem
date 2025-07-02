from model.servico_model import Servico
from repo import servico_repo
import pytest
@pytest.fixture
def servico_exemplo(servicos_exemplo):
    return servicos_exemplo[0]

class TestServicoRepo:
class TestServicoRepo:
    def test_criar_tabela_servicos(self, test_db):
        # Arrange
        # Act
        resultado = servico_repo.criar_tabela_servicos()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_servico(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Assert
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db is not None, "O serviço inserido não deveria ser None"
        assert servico_db.id == id_servico_inserido, "O serviço inserido deveria ter um ID igual ao retornado pela inserção"
        assert servico_db.nome == "Serviço Teste", "O nome do serviço inserido não confere"
        assert servico_db.descricao == "Descrição do serviço", "A descrição do serviço inserido não confere"
        assert servico_db.preco == 100.0, "O preço do serviço inserido não confere"
        assert servico_db.tipo == 0, "O tipo do serviço inserido não confere"

    def test_obter_servico_por_id_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        # Assert
        assert servico_db is not None, "O serviço retornado deveria ser diferente de None"
        assert servico_db.id == id_servico_inserido, "O id do serviço buscado deveria ser igual ao id do serviço inserido"
        assert servico_db.nome == servico_exemplo.nome, "O nome do serviço buscado deveria ser igual ao nome do serviço inserido"
        assert servico_db.descricao == servico_exemplo.descricao, "A descrição do serviço buscado deveria ser igual à descrição do serviço inserido"
        assert servico_db.preco == servico_exemplo.preco, "O preço do serviço buscado deveria ser igual ao preço do serviço inserido"
        assert servico_db.tipo == servico_exemplo.tipo, "O tipo do serviço buscado deveria ser igual ao tipo do serviço inserido"
        assert servico_db.tipo == servico_exemplo.tipo, "O tipo do serviço buscado deveria ser igual ao tipo do serviço inserido"

    def test_obter_servico_por_id_inexistente(self, test_db):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        servico_db = servico_repo.obter_servico_por_id(999)
        # Assert
        assert servico_db is None, "O serviço buscado com ID inexistente deveria retornar None"

    

    def test_atualizar_servico_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        servico_db.nome = "Serviço Atualizado"
        servico_db.descricao = "Descrição Atualizada"
        servico_db.preco = 150.0
        servico_db.tipo = 1
        resultado = servico_repo.atualizar_servico(servico_db)
        # Assert
        assert resultado == True, "A atualização do serviço deveria retornar True"
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db.nome == "Serviço Atualizado", "O nome do serviço atualizado não confere"
        assert servico_db.descricao == "Descrição Atualizada", "A descrição do serviço atualizado não confere"
        assert servico_db.preco == 150.0, "O preço do serviço atualizado não confere"
        assert servico_db.tipo == 1, "O tipo do serviço atualizado não confere"

    def test_atualizar_servico_inexistente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        servico_exemplo.id = 999  # ID que não existe
        # Act
        resultado = servico_repo.atualizar_servico(servico_exemplo)
        # Assert
        assert resultado == False, "A atualização de um serviço inexistente deveria retornar False"

    def test_excluir_servico_existente(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        resultado = servico_repo.excluir_servico(id_servico_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        servico_excluido = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_excluido is None, "O serviço excluído deveria ser None"

    def test_excluir_servico_inexistente(self, test_db):
        # Arrange
        servico_repo.criar_tabela_servicos()
        # Act
        resultado = servico_repo.excluir_servico(999)
        # Assert
        assert resultado == False, "A exclusão de um serviço inexistente deveria retornar False"

    def test_atualizar_tipo_servico(self, test_db, servico_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        id_servico_inserido = servico_repo.inserir_servico(servico_exemplo)
        # Act
        resultado = servico_repo.atualizar_tipo_servico(id_servico_inserido, 1)
        # Assert
        assert resultado == True, "A atualização do tipo de serviço deveria retornar True"
        servico_db = servico_repo.obter_servico_por_id(id_servico_inserido)
        assert servico_db.tipo == 1, "O tipo do serviço atualizado não confere"

   
    def test_obter_servicos_por_pagina_primeira_pagina(self, test_db, lista_servicos_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        for servico in lista_servicos_exemplo:
            servico_repo.inserir_servico(servico)
        # Act
        pagina_servicos = servico_repo.obter_servicos_por_pagina(1, 4)
        # Assert
        assert len(pagina_servicos) == 4, "Deveria retornar 4 serviços na primeira página"
        assert all(isinstance(s, Servico) for s in pagina_servicos), "Todos os itens da página devem ser do tipo Servico"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_servicos]
        assert ids_esperados == ids_retornados, "Os IDs dos serviços na primeira página não estão corretos"

    def test_obter_servicos_por_pagina_terceira_pagina(self, test_db, lista_servicos_exemplo):
        # Arrange
        servico_repo.criar_tabela_servicos()
        for servico in lista_servicos_exemplo:
            servico_repo.inserir_servico(servico)
        # Act: busca a terceira página com 4 serviços por página
        pagina_servicos = servico_repo.obter_servicos_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 serviços na terceira página)
        assert len(pagina_servicos) == 2, "Deveria retornar 2 serviços na terceira página"
        assert (isinstance(s, Servico) for s in pagina_servicos), "Todos os itens da página devem ser do tipo Servico"