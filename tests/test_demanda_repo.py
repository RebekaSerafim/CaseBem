import pytest
from datetime import datetime
from core.models.demanda_model import Demanda
from core.models.casal_model import Casal
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories.demanda_repo import demanda_repo
from core.repositories.casal_repo import casal_repo
from core.repositories.usuario_repo import usuario_repo
from core.repositories.categoria_repo import categoria_repo
from util.exceptions import RecursoNaoEncontradoError

class TestDemandaRepo:
    def test_criar_tabela_demandas(self, test_db):
        # Arrange
        # Act
        resultado = demanda_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_demanda(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        # Inserir usuários e casal
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)
        
        # Act
        id_demanda_inserida = demanda_repo.inserir(demanda_exemplo)
        
        # Assert
        demanda_db = demanda_repo.obter_por_id(id_demanda_inserida)
        assert demanda_db is not None, "A demanda inserida não deveria ser None"
        assert demanda_db.id == id_demanda_inserida, "A demanda inserida deveria ter um ID igual ao retornado pela inserção"
        assert demanda_db.id_casal == 1, "O id_casal da demanda inserida não confere"
        assert demanda_db.data_criacao is not None, "A data_criacao não deveria ser None"

    def test_obter_demanda_por_id_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)
        
        id_demanda_inserida = demanda_repo.inserir(demanda_exemplo)
        
        # Act
        demanda_db = demanda_repo.obter_por_id(id_demanda_inserida)
        
        # Assert
        assert demanda_db is not None, "A demanda retornada deveria ser diferente de None"
        assert demanda_db.id == id_demanda_inserida, "O id da demanda buscada deveria ser igual ao id da demanda inserida"
        assert demanda_db.id_casal == demanda_exemplo.id_casal, "O id_casal da demanda buscada deveria ser igual ao id_casal da demanda inserida"

    def test_obter_demanda_por_id_inexistente(self, test_db):
        # Arrange
        demanda_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            demanda_repo.obter_por_id(999)

    def test_atualizar_demanda_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)
        
        id_demanda_inserida = demanda_repo.inserir(demanda_exemplo)
        
        # Act
        demanda_db = demanda_repo.obter_por_id(id_demanda_inserida)
        # Apenas verificar se a atualização funciona, sem comparar datas
        resultado = demanda_repo.atualizar(demanda_db)
        
        # Assert
        assert resultado == True, "A atualização da demanda deveria retornar True"

    def test_atualizar_demanda_inexistente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)
        
        demanda = Demanda(
            id=999,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda inexistente",
            descricao="Teste de demanda inexistente"
        )
        # Act
        resultado = demanda_repo.atualizar(demanda)
        # Assert
        assert resultado == False, "A atualização de uma demanda inexistente deveria retornar False"

    def test_excluir_demanda_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)
        
        id_demanda_inserida = demanda_repo.inserir(demanda_exemplo)
        
        # Act
        resultado = demanda_repo.excluir(id_demanda_inserida)

        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        with pytest.raises(RecursoNaoEncontradoError):
            demanda_repo.obter_por_id(id_demanda_inserida)

    def test_excluir_demanda_inexistente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)

        # Act
        resultado = demanda_repo.excluir(999)
        # Assert
        assert resultado == False, "A exclusão de uma demanda inexistente deveria retornar False"

    def test_obter_demandas_por_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir usuários e casais
        for usuario in lista_usuarios_exemplo[:10]:
            usuario_repo.inserir(usuario)

        from core.models.casal_model import Casal
        for i in range(1, 11, 2):
            casal = Casal(0, i, i+1)
            casal_repo.inserir(casal)

        # Inserir 5 demandas com categoria válida
        for i in range(5):
            casal_id = (i // 2) + 1  # Distribui entre os 5 casais
            demanda = Demanda(
                id=0,
                id_casal=casal_id,
                id_categoria=id_categoria,
                titulo=f"Demanda {i+1}",
                descricao=f"Descrição da demanda {i+1}"
            )
            demanda_repo.inserir(demanda)

        # Act
        pagina_demandas = demanda_repo.obter_por_pagina(1, 3)

        # Assert
        assert len(pagina_demandas) <= 3, "Deveria retornar no máximo 3 demandas na primeira página"
        assert len(pagina_demandas) > 0, "Deveria retornar pelo menos 1 demanda"
        assert all(isinstance(d, Demanda) for d in pagina_demandas), "Todos os itens da página devem ser do tipo Demanda"

    def test_obter_demandas_por_casal(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        # Inserir usuários e casal
        for noivo in lista_noivos_exemplo[:4]:
            usuario_repo.inserir(noivo)
        
        from core.models.casal_model import Casal
        casal1 = Casal(0, 1, 2)
        casal2 = Casal(0, 3, 4)
        id_casal1 = casal_repo.inserir(casal1)
        id_casal2 = casal_repo.inserir(casal2)
        
        # Inserir demandas para casal1
        demanda1 = Demanda(
            id=0,
            id_casal=id_casal1,
            id_categoria=1,
            titulo="Demanda 1",
            descricao="Descrição da demanda 1"
        )
        demanda2 = Demanda(
            id=0,
            id_casal=id_casal1,
            id_categoria=1,
            titulo="Demanda 2",
            descricao="Descrição da demanda 2"
        )
        demanda3 = Demanda(
            id=0,
            id_casal=id_casal2,
            id_categoria=1,
            titulo="Demanda 3",
            descricao="Descrição da demanda 3"
        )
        
        demanda_repo.inserir(demanda1)
        demanda_repo.inserir(demanda2)
        demanda_repo.inserir(demanda3)
        
        # Act
        demandas_casal1 = demanda_repo.obter_por_casal(id_casal1)
        
        # Assert
        assert len(demandas_casal1) == 2, "Deveria retornar 2 demandas para o casal1"
        assert all(d.id_casal == id_casal1 for d in demandas_casal1), "Todas as demandas devem pertencer ao casal1"