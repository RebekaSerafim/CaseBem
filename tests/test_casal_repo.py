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
        novo_casal = Casal(1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        # Act
        ids_noivos = casal_repo.inserir_casal(novo_casal)        
        # Assert
        assert ids_noivos is not None, "ID do casal inserido não pode ser None"
        casal = casal_repo.obter_casal_por_ids(ids_noivos[0], ids_noivos[1])
        assert casal is not None, "Casal não encontrado após inserção"
        assert casal.id_noivo1 == 1
        assert casal.id_noivo2 == 2
        assert casal.orcamento == 10000.0

    def test_obter_casal_por_id_inexistente(self, test_db):
        # Arrange        
        casal_repo.criar_tabela_casal()
        # Act        
        casal = casal_repo.obter_casal_por_ids(1, 2)
        # Assert
        assert casal is None, "Não deveria encontrar casal com IDs inexistentes"
        

    def test_atualizar_casal_existente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        ids_noivos = casal_repo.inserir_casal(novo_casal)
        # Act
        casal_atualizado = Casal(ids_noivos[0], ids_noivos[1], 15000.0)
        sucesso = casal_repo.atualizar_casal(casal_atualizado)
        # Assert
        assert sucesso is True, "Atualização do casal deveria ser bem-sucedida"
        casal = casal_repo.obter_casal_por_ids(ids_noivos[0], ids_noivos[1])
        assert casal is not None, "Casal não encontrado após atualização"
        assert casal.orcamento == 15000.0, "Orçamento do casal não foi atualizado corretamente"

    def test_atualizar_casal_inexistente(self, test_db):
        # Arrange
        casal_repo.criar_tabela_casal()
        # Act
        noivo_exemplo = Casal(1, 2, 10000.0)        
        atualizou = casal_repo.atualizar_casal(noivo_exemplo)
        # Assert
        assert atualizou is False, "Atualização de casal inexistente deveria falhar"

    def test_excluir_casal_existente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        for noivo in lista_noivos_exemplo:
            usuario_repo.inserir_usuario(noivo)
        novo_casal = Casal(1, 2, 10000.0)
        casal_repo.criar_tabela_casal()
        ids_noivos = casal_repo.inserir_casal(novo_casal)
        # Act
        casal_atualizado = Casal(ids_noivos[0], ids_noivos[1], 15000.0)
        sucesso = casal_repo.excluir_casal(casal_atualizado)
        # Assert
        assert sucesso is True, "Atualização do casal deveria ser bem-sucedida"
        casal_excluido = casal_repo.obter_casal_por_ids(ids_noivos[0], ids_noivos[1])
        assert casal_excluido is None, "Casal não foi excluído corretamente"

    def test_excluir_casal_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        casal = Casal(999, 1000, 5000.0)
        assert casal_repo.excluir_casal(casal) is False

    def test_obter_casais_por_pagina(self, test_db, lista_usuarios_exemplo, lista_casais_exemplo):
        usuario_repo.criar_tabela_usuarios()
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        casal_repo.criar_tabela_casal()
        for n in lista_casais_exemplo:
            casal_repo.inserir_casal(n)
        pagina = casal_repo.obter_casais_por_pagina(1, 4)
        assert all(isinstance(n, Casal) for n in pagina)