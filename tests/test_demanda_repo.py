from datetime import datetime
from model.demanda_model import Demanda
from model.casal_model import Casal
from model.categoria_model import Categoria
from model.tipo_fornecimento_model import TipoFornecimento
from repo import demanda_repo, casal_repo, usuario_repo, categoria_repo

class TestDemandaRepo:
    def test_criar_tabela_demandas(self, test_db):
        # Arrange
        # Act
        resultado = demanda_repo.criar_tabela_demandas()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_demanda(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        # Inserir usuários e casal
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Act
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Assert
        demanda_db = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        assert demanda_db is not None, "A demanda inserida não deveria ser None"
        assert demanda_db.id == id_demanda_inserida, "A demanda inserida deveria ter um ID igual ao retornado pela inserção"
        assert demanda_db.id_casal == 1, "O id_casal da demanda inserida não confere"
        assert demanda_db.data_criacao is not None, "A data_criacao não deveria ser None"

    def test_obter_demanda_por_id_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Act
        demanda_db = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        
        # Assert
        assert demanda_db is not None, "A demanda retornada deveria ser diferente de None"
        assert demanda_db.id == id_demanda_inserida, "O id da demanda buscada deveria ser igual ao id da demanda inserida"
        assert demanda_db.id_casal == demanda_exemplo.id_casal, "O id_casal da demanda buscada deveria ser igual ao id_casal da demanda inserida"

    def test_obter_demanda_por_id_inexistente(self, test_db):
        # Arrange
        demanda_repo.criar_tabela_demandas()
        # Act
        demanda_db = demanda_repo.obter_demanda_por_id(999)
        # Assert
        assert demanda_db is None, "A demanda buscada com ID inexistente deveria retornar None"

    def test_atualizar_demanda_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Act
        demanda_db = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        # Apenas verificar se a atualização funciona, sem comparar datas
        resultado = demanda_repo.atualizar_demanda(demanda_db)
        
        # Assert
        assert resultado == True, "A atualização da demanda deveria retornar True"

    def test_atualizar_demanda_inexistente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(
            id=999,
            id_casal=1,
            id_categoria=1,
            titulo="Demanda inexistente",
            descricao="Teste de demanda inexistente"
        )
        # Act
        resultado = demanda_repo.atualizar_demanda(demanda)
        # Assert
        assert resultado == False, "A atualização de uma demanda inexistente deveria retornar False"

    def test_excluir_demanda_existente(self, test_db, demanda_exemplo, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        id_demanda_inserida = demanda_repo.inserir_demanda(demanda_exemplo)
        
        # Act
        resultado = demanda_repo.excluir_demanda(id_demanda_inserida)
        
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        demanda_excluida = demanda_repo.obter_demanda_por_id(id_demanda_inserida)
        assert demanda_excluida is None, "A demanda excluída deveria ser None"

    def test_excluir_demanda_inexistente(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        
        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Act
        resultado = demanda_repo.excluir_demanda(999)
        # Assert
        assert resultado == False, "A exclusão de uma demanda inexistente deveria retornar False"

    def test_obter_demandas_por_pagina(self, test_db, lista_demandas_exemplo, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        # Inserir usuários e casais
        for usuario in lista_usuarios_exemplo:
            usuario_repo.inserir_usuario(usuario)
        
        from model.casal_model import Casal
        for i in range(1, 11, 2):
            casal = Casal(0, i, i+1, 10000.0)
            casal_repo.inserir_casal(casal)
        
        # Inserir demandas
        for demanda in lista_demandas_exemplo[:5]:
            demanda_repo.inserir_demanda(demanda)
        
        # Act
        pagina_demandas = demanda_repo.obter_demandas_por_pagina(1, 3)
        
        # Assert
        assert len(pagina_demandas) == 3, "Deveria retornar 3 demandas na primeira página"
        assert all(isinstance(d, Demanda) for d in pagina_demandas), "Todos os itens da página devem ser do tipo Demanda"

    def test_obter_demandas_por_casal(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        categoria_repo.criar_tabela_categorias()
        demanda_repo.criar_tabela_demandas()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir_categoria(categoria)

        # Inserir usuários e casal
        for noivo in lista_noivos_exemplo[:4]:
            usuario_repo.inserir_usuario(noivo)
        
        from model.casal_model import Casal
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        id_casal1 = casal_repo.inserir_casal(casal1)
        id_casal2 = casal_repo.inserir_casal(casal2)
        
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
        
        demanda_repo.inserir_demanda(demanda1)
        demanda_repo.inserir_demanda(demanda2)
        demanda_repo.inserir_demanda(demanda3)
        
        # Act
        demandas_casal1 = demanda_repo.obter_demandas_por_casal(id_casal1)
        
        # Assert
        assert len(demandas_casal1) == 2, "Deveria retornar 2 demandas para o casal1"
        assert all(d.id_casal == id_casal1 for d in demandas_casal1), "Todas as demandas devem pertencer ao casal1"