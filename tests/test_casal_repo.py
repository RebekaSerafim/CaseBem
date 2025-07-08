from model.casal_model import Casal
from repo import casal_repo, usuario_repo

class TestCasalRepo:
    def test_criar_tabela_casal(self, test_db):
        assert casal_repo.criar_tabela_casal() is True

    def test_inserir_casal(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(0, 1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        # Act
        id_casal = casal_repo.inserir_casal(novo_casal)        
        # Assert
        assert id_casal is not None, "ID do casal inserido não pode ser None"
        casal = casal_repo.obter_casal_por_id(id_casal)
        assert casal is not None, "Casal não encontrado após inserção"
        assert casal.id_noivo1 == 1
        assert casal.id_noivo2 == 2
        assert casal.orcamento == 10000.0

    def test_obter_casal_por_id_inexistente(self, test_db):
        # Arrange        
        casal_repo.criar_tabela_casal()
        # Act        
        casal = casal_repo.obter_casal_por_id(999)
        # Assert
        assert casal is None, "Não deveria encontrar casal com ID inexistente"

    def test_atualizar_casal_existente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(0, 1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        id_casal = casal_repo.inserir_casal(novo_casal)
        # Act
        casal_atualizado = Casal(id_casal, 1, 2, 15000.0)
        sucesso = casal_repo.atualizar_casal(casal_atualizado)
        # Assert
        assert sucesso is True, "Atualização do casal deveria ser bem-sucedida"
        casal = casal_repo.obter_casal_por_id(id_casal)
        assert casal is not None, "Casal não encontrado após atualização"
        assert casal.orcamento == 15000.0, "Orçamento do casal não foi atualizado corretamente"

    def test_atualizar_casal_inexistente(self, test_db):
        # Arrange
        casal_repo.criar_tabela_casal()
        # Act
        casal_inexistente = Casal(999, 1, 2, 10000.0)        
        atualizou = casal_repo.atualizar_casal(casal_inexistente)
        # Assert
        assert atualizou is False, "Atualização de casal inexistente deveria falhar"

    def test_excluir_casal_existente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(0, 1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        id_casal = casal_repo.inserir_casal(novo_casal)
        # Act
        sucesso = casal_repo.excluir_casal(id_casal)
        # Assert
        assert sucesso is True, "Exclusão do casal deveria ser bem-sucedida"
        casal_excluido = casal_repo.obter_casal_por_id(id_casal)
        assert casal_excluido is None, "Casal não foi excluído corretamente"

    def test_excluir_casal_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        assert casal_repo.excluir_casal(999) is False

    def test_obter_casais_por_pagina(self, test_db, lista_usuarios_exemplo, lista_casais_exemplo):
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        casal_repo.criar_tabela_casal()
        for casal in lista_casais_exemplo:
            casal_repo.inserir_casal(casal)
        pagina = casal_repo.obter_casais_por_pagina(1, 4)
        assert len(pagina) == 4
        assert all(isinstance(c, Casal) for c in pagina)

    def test_obter_casal_por_noivo(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        casal_repo.criar_tabela_casal()
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        casal_repo.inserir_casal(casal1)
        casal_repo.inserir_casal(casal2)
        # Act
        casal_encontrado = casal_repo.obter_casal_por_noivo(1)
        # Assert
        assert casal_encontrado is not None
        assert casal_encontrado.id_noivo1 == 1 or casal_encontrado.id_noivo2 == 1