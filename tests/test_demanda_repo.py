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
        categoria = Categoria(
            0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True
        )
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
        assert (
            demanda_db.id == id_demanda_inserida
        ), "A demanda inserida deveria ter um ID igual ao retornado pela inserção"
        assert demanda_db.id_casal == 1, "O id_casal da demanda inserida não confere"
        assert (
            demanda_db.data_criacao is not None
        ), "A data_criacao não deveria ser None"

    def test_obter_demanda_por_id_existente(
        self, test_db, demanda_exemplo, lista_noivos_exemplo
    ):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(
            0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True
        )
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)

        id_demanda_inserida = demanda_repo.inserir(demanda_exemplo)

        # Act
        demanda_db = demanda_repo.obter_por_id(id_demanda_inserida)

        # Assert
        assert (
            demanda_db is not None
        ), "A demanda retornada deveria ser diferente de None"
        assert (
            demanda_db.id == id_demanda_inserida
        ), "O id da demanda buscada deveria ser igual ao id da demanda inserida"
        assert (
            demanda_db.id_casal == demanda_exemplo.id_casal
        ), "O id_casal da demanda buscada deveria ser igual ao id_casal da demanda inserida"

    def test_obter_demanda_por_id_inexistente(self, test_db):
        # Arrange
        demanda_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            demanda_repo.obter_por_id(999)

    def test_atualizar_demanda_existente(
        self, test_db, demanda_exemplo, lista_noivos_exemplo
    ):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(
            0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True
        )
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
        demanda_repo.criar_tabela()

        # Criar usuários e casal necessários para satisfazer foreign key
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        casal_repo.inserir(casal)

        demanda = Demanda(
            id=999,
            id_casal=1,
            descricao="Teste de demanda inexistente",
            orcamento_total=5000.00,
            data_casamento="2025-12-31",
            cidade_casamento="Vitória",
        )
        # Act
        resultado = demanda_repo.atualizar(demanda)
        # Assert
        assert (
            resultado == False
        ), "A atualização de uma demanda inexistente deveria retornar False"

    def test_excluir_demanda_existente(
        self, test_db, demanda_exemplo, lista_noivos_exemplo
    ):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(
            0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True
        )
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
        assert (
            resultado == False
        ), "A exclusão de uma demanda inexistente deveria retornar False"

    def test_obter_demandas_por_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()

        # Inserir usuários e casais
        for usuario in lista_usuarios_exemplo[:10]:
            usuario_repo.inserir(usuario)

        from core.models.casal_model import Casal

        for i in range(1, 11, 2):
            casal = Casal(0, i, i + 1)
            casal_repo.inserir(casal)

        # Inserir 5 demandas
        for i in range(5):
            casal_id = (i // 2) + 1  # Distribui entre os 5 casais
            demanda = Demanda(
                id=0,
                id_casal=casal_id,
                descricao=f"Descrição da demanda {i+1}",
                orcamento_total=round((i + 1) * 1000.0, 2),
                data_casamento="2025-12-31",
                cidade_casamento="Vitória",
            )
            demanda_repo.inserir(demanda)

        # Act
        pagina_demandas = demanda_repo.obter_por_pagina(1, 3)

        # Assert
        assert (
            len(pagina_demandas) <= 3
        ), "Deveria retornar no máximo 3 demandas na primeira página"
        assert len(pagina_demandas) > 0, "Deveria retornar pelo menos 1 demanda"
        assert all(
            isinstance(d, Demanda) for d in pagina_demandas
        ), "Todos os itens da página devem ser do tipo Demanda"

    def test_obter_demandas_por_casal(self, test_db, lista_noivos_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()

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
            descricao="Descrição da demanda 1",
            orcamento_total=3000.00,
            data_casamento="2025-12-31",
            cidade_casamento="Vitória",
        )
        demanda2 = Demanda(
            id=0,
            id_casal=id_casal1,
            descricao="Descrição da demanda 2",
            orcamento_total=5000.00,
            data_casamento="2025-12-31",
            cidade_casamento="Vila Velha",
        )
        demanda3 = Demanda(
            id=0,
            id_casal=id_casal2,
            descricao="Descrição da demanda 3",
            orcamento_total=4000.00,
            data_casamento="2026-01-15",
            cidade_casamento="Cachoeiro",
        )

        demanda_repo.inserir(demanda1)
        demanda_repo.inserir(demanda2)
        demanda_repo.inserir(demanda3)

        # Act
        demandas_casal1 = demanda_repo.obter_por_casal(id_casal1)

        # Assert
        assert len(demandas_casal1) == 2, "Deveria retornar 2 demandas para o casal1"
        assert all(
            d.id_casal == id_casal1 for d in demandas_casal1
        ), "Todas as demandas devem pertencer ao casal1"

    def test_atualizar_status(self, test_db, lista_noivos_exemplo):
        """Testa atualização de status da demanda (linha 57)"""
        from core.models.demanda_model import StatusDemanda

        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=id_casal,
            descricao="Demanda teste",
            status=StatusDemanda.ATIVA,
        )
        id_demanda = demanda_repo.inserir(demanda)
        # Act
        resultado = demanda_repo.atualizar_status(id_demanda, StatusDemanda.FINALIZADA)
        # Assert
        assert resultado is True, "Atualização de status deveria retornar True"
        demanda_db = demanda_repo.obter_por_id(id_demanda)
        assert demanda_db.status == StatusDemanda.FINALIZADA

    def test_obter_ativas(self, test_db, lista_noivos_exemplo):
        """Testa obtenção de demandas ativas (linhas 70-71)"""
        from core.models.demanda_model import StatusDemanda

        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda1 = Demanda(id=0, id_casal=id_casal, descricao="Demanda 1")
        demanda2 = Demanda(id=0, id_casal=id_casal, descricao="Demanda 2")
        id_demanda1 = demanda_repo.inserir(demanda1)
        id_demanda2 = demanda_repo.inserir(demanda2)
        # Atualizar status da segunda demanda para CANCELADA
        demanda_repo.atualizar_status(id_demanda2, StatusDemanda.CANCELADA)
        # Act
        demandas_ativas = demanda_repo.obter_ativas()
        # Assert
        assert len(demandas_ativas) == 1, "Deveria retornar apenas 1 demanda ativa"
        assert demandas_ativas[0].status == StatusDemanda.ATIVA
        assert demandas_ativas[0].id == id_demanda1

    def test_buscar_demandas(self, test_db, lista_noivos_exemplo):
        """Testa busca de demandas por termo (linhas 75-79)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda1 = Demanda(
            id=0, id_casal=id_casal, descricao="Decoração especial para casamento"
        )
        demanda2 = Demanda(id=0, id_casal=id_casal, descricao="Buffet completo")
        demanda3 = Demanda(id=0, id_casal=id_casal, descricao="Decoração simples")
        demanda_repo.inserir(demanda1)
        demanda_repo.inserir(demanda2)
        demanda_repo.inserir(demanda3)
        # Act
        resultados = demanda_repo.buscar("Decoração")
        # Assert
        assert len(resultados) == 2, "Deveria encontrar 2 demandas com 'Decoração'"
        assert all("Decoração" in d.descricao for d in resultados)

    def test_obter_por_status_com_enum(self, test_db, lista_noivos_exemplo):
        """Testa obtenção por status usando enum (linhas 84-101)"""
        from core.models.demanda_model import StatusDemanda

        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda1 = Demanda(id=0, id_casal=id_casal, descricao="Demanda 1")
        demanda2 = Demanda(id=0, id_casal=id_casal, descricao="Demanda 2")
        demanda3 = Demanda(id=0, id_casal=id_casal, descricao="Demanda 3")
        demanda_repo.inserir(demanda1)
        demanda_repo.inserir(demanda2)
        id_demanda3 = demanda_repo.inserir(demanda3)
        # Atualizar status da terceira demanda para FINALIZADA
        demanda_repo.atualizar_status(id_demanda3, StatusDemanda.FINALIZADA)
        # Act
        demandas_ativas = demanda_repo.obter_por_status(StatusDemanda.ATIVA)
        # Assert
        assert len(demandas_ativas) == 2, "Deveria retornar 2 demandas ativas"
        assert all(d.status == StatusDemanda.ATIVA for d in demandas_ativas)

    def test_obter_por_status_com_string(self, test_db, lista_noivos_exemplo):
        """Testa obtenção por status usando string (linhas 87-96)"""
        from core.models.demanda_model import StatusDemanda

        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda1 = Demanda(id=0, id_casal=id_casal, descricao="Demanda 1")
        id_demanda1 = demanda_repo.inserir(demanda1)
        # Atualizar status para FINALIZADA
        demanda_repo.atualizar_status(id_demanda1, StatusDemanda.FINALIZADA)
        # Act
        demandas = demanda_repo.obter_por_status("finalizada")
        # Assert
        assert len(demandas) == 1, "Deveria retornar 1 demanda finalizada"
        assert demandas[0].status == StatusDemanda.FINALIZADA

    def test_obter_por_status_invalido(self, test_db, lista_noivos_exemplo):
        """Testa obtenção por status inválido (linhas 92-96)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda = Demanda(id=0, id_casal=id_casal, descricao="Demanda teste")
        demanda_repo.inserir(demanda)
        # Act
        demandas = demanda_repo.obter_por_status("INVALIDO")
        # Assert
        assert len(demandas) == 0, "Deveria retornar lista vazia para status inválido"

    def test_obter_por_cidade(self, test_db, lista_noivos_exemplo):
        """Testa obtenção de demandas por cidade (linhas 116-119)"""
        from core.models.demanda_model import StatusDemanda

        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        casal = Casal(0, 1, 2)
        id_casal = casal_repo.inserir(casal)
        demanda1 = Demanda(
            id=0,
            id_casal=id_casal,
            descricao="Demanda 1",
            cidade_casamento="Vitória",
            status=StatusDemanda.ATIVA,
        )
        demanda2 = Demanda(
            id=0,
            id_casal=id_casal,
            descricao="Demanda 2",
            cidade_casamento="Vitória",
            status=StatusDemanda.ATIVA,
        )
        demanda3 = Demanda(
            id=0,
            id_casal=id_casal,
            descricao="Demanda 3",
            cidade_casamento="Vila Velha",
            status=StatusDemanda.ATIVA,
        )
        demanda_repo.inserir(demanda1)
        demanda_repo.inserir(demanda2)
        demanda_repo.inserir(demanda3)
        # Act
        demandas_vitoria = demanda_repo.obter_por_cidade("Vitória")
        # Assert
        assert len(demandas_vitoria) == 2, "Deveria retornar 2 demandas de Vitória"
        assert all(d.cidade_casamento == "Vitória" for d in demandas_vitoria)
