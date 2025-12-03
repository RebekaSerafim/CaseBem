import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from core.models.orcamento_model import Orcamento
from core.models.demanda_model import Demanda
from core.models.casal_model import Casal
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories.orcamento_repo import orcamento_repo
from core.repositories.demanda_repo import demanda_repo
from core.repositories.casal_repo import casal_repo
from core.repositories.usuario_repo import usuario_repo
from core.repositories.categoria_repo import categoria_repo
from core.repositories.item_orcamento_repo import item_orcamento_repo
from core.repositories.item_repo import item_repo
from core.repositories.item_demanda_repo import item_demanda_repo
from core.models.item_orcamento_model import ItemOrcamento
from core.models.item_model import Item
from core.models.item_demanda_model import ItemDemanda
from util.exceptions import RecursoNaoEncontradoError

class TestOrcamentoRepo:
    def test_criar_tabela_orcamento(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        demanda_repo.criar_tabela()
        # Agora criar tabela orcamento
        assert orcamento_repo.criar_tabela() is True

    def test_inserir_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        # Criar orçamento
        orcamento = Orcamento(
            id=0,
            id_demanda=id_demanda,
            id_fornecedor_prestador=id_fornecedor,
            data_hora_cadastro=datetime.now(),
            data_hora_validade=datetime.now() + timedelta(days=30),
            status="PENDENTE",
            observacoes="Orçamento de teste",
            valor_total=1500.00
        )
        
        # Act
        id_orcamento = orcamento_repo.inserir(orcamento)
        
        # Assert
        assert id_orcamento is not None
        orcamento_salvo = orcamento_repo.obter_por_id(id_orcamento)
        assert orcamento_salvo is not None
        assert orcamento_salvo.id_demanda == id_demanda
        assert orcamento_salvo.id_fornecedor_prestador == id_fornecedor
        assert orcamento_salvo.status == "PENDENTE"
        assert orcamento_salvo.valor_total == 1500.00

    def test_atualizar_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), 
                            datetime.now() + timedelta(days=30), "PENDENTE", 
                            "Orçamento inicial", 1500.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        
        # Act
        orcamento_atualizado = orcamento_repo.obter_por_id(id_orcamento)
        orcamento_atualizado.status = "ACEITO"
        orcamento_atualizado.valor_total = 2000.00
        orcamento_atualizado.observacoes = "Orçamento atualizado"
        sucesso = orcamento_repo.atualizar(orcamento_atualizado)
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_por_id(id_orcamento)
        assert orcamento_verificado.status == "ACEITO"
        assert orcamento_verificado.valor_total == 2000.00
        assert orcamento_verificado.observacoes == "Orçamento atualizado"

    def test_atualizar_status_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir(orcamento)
        
        # Act
        sucesso = orcamento_repo.atualizar_status(id_orcamento, "ACEITO")
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_por_id(id_orcamento)
        assert orcamento_verificado.status == "ACEITO"

    def test_atualizar_valor_total_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 100.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        
        # Act
        sucesso = orcamento_repo.atualizar_valor_total(id_orcamento, 250.00)
        
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_por_id(id_orcamento)
        assert orcamento_verificado.valor_total == 250.00

    def test_aceitar_orcamento_e_rejeitar_outros(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        # Inserir múltiplos orçamentos
        ids_orcamentos = []
        for i, id_fornecedor in enumerate(ids_fornecedores):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            ids_orcamentos.append(orcamento_repo.inserir(orcamento))
        
        # Act - Aceitar o segundo orçamento
        sucesso = orcamento_repo.aceitar_e_rejeitar_outros(ids_orcamentos[1], id_demanda)
        
        # Assert
        assert sucesso is True
        # Verificar que o segundo foi aceito
        orcamento_aceito = orcamento_repo.obter_por_id(ids_orcamentos[1])
        assert orcamento_aceito.status == "ACEITO"
        
        # Verificar que os outros foram rejeitados
        orcamento_rejeitado1 = orcamento_repo.obter_por_id(ids_orcamentos[0])
        assert orcamento_rejeitado1.status == "REJEITADO"
        
        orcamento_rejeitado2 = orcamento_repo.obter_por_id(ids_orcamentos[2])
        assert orcamento_rejeitado2.status == "REJEITADO"

    def test_excluir_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir(orcamento)
        
        # Act
        sucesso = orcamento_repo.excluir(id_orcamento)

        # Assert
        assert sucesso is True
        with pytest.raises(RecursoNaoEncontradoError):
            orcamento_repo.obter_por_id(id_orcamento)

    def test_obter_orcamento_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            orcamento_repo.obter_por_id(999)

    def test_obter_orcamentos_por_demanda(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        # Inserir orçamentos
        for i, id_fornecedor in enumerate(ids_fornecedores):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            orcamento_repo.inserir(orcamento)
        
        # Act
        orcamentos = orcamento_repo.obter_por_demanda(id_demanda)
        
        # Assert
        assert len(orcamentos) == 3
        assert all(o.id_demanda == id_demanda for o in orcamentos)

    def test_obter_orcamentos_por_fornecedor_prestador(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)

        # Inserir fornecedor (precisa inserir em ambas as tabelas)
        from core.repositories.fornecedor_repo import fornecedor_repo
        fornecedor_repo.criar_tabela()
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        
        # Criar múltiplas demandas
        ids_demandas = []
        for i in range(3):
            demanda = Demanda(
                id=0,
                id_casal=1,
                descricao="Descrição da demanda de teste"
            )
            ids_demandas.append(demanda_repo.inserir(demanda))
        
        # Inserir orçamentos do mesmo fornecedor
        assert id_fornecedor is not None
        for id_demanda in ids_demandas:
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None,
                                "PENDENTE", None, 100.00)
            orcamento_repo.inserir(orcamento)

        # Act
        orcamentos = orcamento_repo.obter_por_fornecedor_prestador(id_fornecedor)
        
        # Assert
        assert len(orcamentos) == 3
        assert all(o.id_fornecedor_prestador == id_fornecedor for o in orcamentos)

    def test_obter_orcamentos_por_status(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        # Inserir orçamentos com status diferentes
        status_list = ["PENDENTE", "ACEITO", "PENDENTE"]
        for i, (id_fornecedor, status) in enumerate(zip(ids_fornecedores, status_list)):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, 
                                status, None, 100.00)
            orcamento_repo.inserir(orcamento)
        
        # Act
        orcamentos_pendentes = orcamento_repo.obter_por_status("PENDENTE")
        orcamentos_aceitos = orcamento_repo.obter_por_status("ACEITO")
        
        # Assert
        assert len(orcamentos_pendentes) == 2
        assert all(o.status == "PENDENTE" for o in orcamentos_pendentes)
        assert len(orcamentos_aceitos) == 1
        assert all(o.status == "ACEITO" for o in orcamentos_aceitos)

    def test_obter_orcamentos_por_pagina(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()

        # Inserir categoria
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)

        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:5]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        
        casal = Casal(
            id=0,
            id_noivo1=1,
            id_noivo2=2,
            data_casamento=None,
            local_previsto=None,
            orcamento_estimado="50k_100k",
            numero_convidados=100
        )
        casal_repo.inserir(casal)
        demanda = Demanda(
            id=0,
            id_casal=1,
            descricao="Descrição da demanda de teste"
        )
        id_demanda = demanda_repo.inserir(demanda)
        
        # Inserir 10 orçamentos
        for i in range(10):
            orcamento = Orcamento(0, id_demanda, ids_fornecedores[i % 5], datetime.now(), 
                                None, "PENDENTE", f"Orçamento {i+1}", 100.0 * (i+1))
            orcamento_repo.inserir(orcamento)
        
        # Act
        pagina1 = orcamento_repo.obter_por_pagina(1, 5)
        pagina2 = orcamento_repo.obter_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 5
        assert all(isinstance(o, Orcamento) for o in pagina1)
        assert all(isinstance(o, Orcamento) for o in pagina2)

    def test_rejeitar_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa rejeição de orçamento (linha 72)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 100.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        # Act
        sucesso = orcamento_repo.rejeitar(id_orcamento)
        # Assert
        assert sucesso is True
        orcamento_verificado = orcamento_repo.obter_por_id(id_orcamento)
        assert orcamento_verificado.status == "REJEITADO"

    def test_obter_orcamentos_por_noivo(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        """Testa obtenção de orçamentos por noivo (linhas 93-96)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:4]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:2]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        # Criar dois casais
        casal1 = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal2 = Casal(0, 3, 4, None, None, "50k_100k", 100)
        id_casal1 = casal_repo.inserir(casal1)
        id_casal2 = casal_repo.inserir(casal2)
        # Criar demandas para cada casal
        demanda1 = Demanda(0, id_casal1, "Demanda do casal 1")
        demanda2 = Demanda(0, id_casal2, "Demanda do casal 2")
        id_demanda1 = demanda_repo.inserir(demanda1)
        id_demanda2 = demanda_repo.inserir(demanda2)
        # Criar orçamentos para cada demanda
        orcamento1 = Orcamento(0, id_demanda1, ids_fornecedores[0], datetime.now(), None, "PENDENTE", None, 100.00)
        orcamento2 = Orcamento(0, id_demanda1, ids_fornecedores[1], datetime.now(), None, "PENDENTE", None, 150.00)
        orcamento3 = Orcamento(0, id_demanda2, ids_fornecedores[0], datetime.now(), None, "PENDENTE", None, 200.00)
        orcamento_repo.inserir(orcamento1)
        orcamento_repo.inserir(orcamento2)
        orcamento_repo.inserir(orcamento3)
        # Act - Obter orçamentos do noivo 1 (que faz parte do casal1)
        orcamentos_noivo1 = orcamento_repo.obter_por_noivo(1)
        # Assert
        assert len(orcamentos_noivo1) == 2, "Noivo 1 deveria ter 2 orçamentos"
        assert all(o.id_demanda == id_demanda1 for o in orcamentos_noivo1)

    def test_contar_orcamentos_por_demanda(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        """Testa contagem de orçamentos por demanda (linhas 114-118)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:3]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        # Inserir 3 orçamentos
        for id_fornecedor in ids_fornecedores:
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 100.00)
            orcamento_repo.inserir(orcamento)
        # Act
        total = orcamento_repo.contar_por_demanda(id_demanda)
        # Assert
        assert total == 3, "Deveria contar 3 orçamentos para a demanda"

    def test_contar_orcamentos_por_demanda_e_status(self, test_db, lista_noivos_exemplo, lista_fornecedores_exemplo):
        """Testa contagem de orçamentos por demanda e status (linhas 122-126)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        ids_fornecedores = []
        for fornecedor in lista_fornecedores_exemplo[:4]:
            ids_fornecedores.append(usuario_repo.inserir(fornecedor))
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        # Inserir orçamentos com status diferentes
        status_list = ["PENDENTE", "ACEITO", "PENDENTE", "REJEITADO"]
        for id_fornecedor, status in zip(ids_fornecedores, status_list):
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, status, None, 100.00)
            orcamento_repo.inserir(orcamento)
        # Act
        total_pendentes = orcamento_repo.contar_por_demanda_e_status(id_demanda, "PENDENTE")
        total_aceitos = orcamento_repo.contar_por_demanda_e_status(id_demanda, "ACEITO")
        # Assert
        assert total_pendentes == 2, "Deveria contar 2 orçamentos pendentes"
        assert total_aceitos == 1, "Deveria contar 1 orçamento aceito"

    def test_calcular_status_derivado_sem_itens(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa cálculo de status derivado sem itens - retorna PENDENTE (linhas 151-152)"""
        # Arrange
        usuario_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 100.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        # Act - Orçamento sem itens
        status = orcamento_repo.calcular_status_derivado(id_orcamento)
        # Assert
        assert status == "PENDENTE", "Orçamento sem itens deveria retornar PENDENTE"

    def test_calcular_status_derivado_todos_aceitos(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa cálculo de status derivado com todos itens aceitos - retorna ACEITO (linhas 155-156)"""
        # Arrange
        usuario_repo.criar_tabela()
        from core.repositories.fornecedor_repo import fornecedor_repo
        fornecedor_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        assert id_demanda is not None
        # Criar item no catálogo
        assert id_fornecedor is not None
        item_catalogo = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste", "Descrição", Decimal("100.00"), id_categoria)
        id_item = item_repo.inserir(item_catalogo)
        assert id_item is not None
        # Criar orçamento
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 300.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        assert id_orcamento is not None
        # Criar 3 item_demandas diferentes para evitar UNIQUE constraint violation
        for i in range(3):
            item_demanda = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, f"Item solicitado {i+1}", 1)
            id_item_demanda = item_demanda_repo.inserir(item_demanda)
            assert id_item_demanda is not None
            item_orc = ItemOrcamento(0, id_orcamento, id_item_demanda, id_item, 1, 100.00, None, None, "ACEITO")
            item_orcamento_repo.inserir(item_orc)
        # Act
        status = orcamento_repo.calcular_status_derivado(id_orcamento)
        # Assert
        assert status == "ACEITO", "Todos itens aceitos deveria retornar ACEITO"

    def test_calcular_status_derivado_todos_rejeitados(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa cálculo de status derivado com todos itens rejeitados - retorna REJEITADO (linhas 159-160)"""
        # Arrange
        usuario_repo.criar_tabela()
        from core.repositories.fornecedor_repo import fornecedor_repo
        fornecedor_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        assert id_demanda is not None
        assert id_fornecedor is not None
        item_catalogo = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste", "Descrição", Decimal("100.00"), id_categoria)
        id_item = item_repo.inserir(item_catalogo)
        assert id_item is not None
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 200.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        assert id_orcamento is not None
        # Criar 2 item_demandas diferentes para evitar UNIQUE constraint violation
        for i in range(2):
            item_demanda = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, f"Item solicitado {i+1}", 1)
            id_item_demanda = item_demanda_repo.inserir(item_demanda)
            assert id_item_demanda is not None
            item_orc = ItemOrcamento(0, id_orcamento, id_item_demanda, id_item, 1, 100.00, None, None, "REJEITADO")
            item_orcamento_repo.inserir(item_orc)
        # Act
        status = orcamento_repo.calcular_status_derivado(id_orcamento)
        # Assert
        assert status == "REJEITADO", "Todos itens rejeitados deveria retornar REJEITADO"

    def test_calcular_status_derivado_todos_pendentes(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa cálculo de status derivado com todos itens pendentes - retorna PENDENTE (linhas 163-164)"""
        # Arrange
        usuario_repo.criar_tabela()
        from core.repositories.fornecedor_repo import fornecedor_repo
        fornecedor_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        assert id_demanda is not None
        assert id_fornecedor is not None
        item_catalogo = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste", "Descrição", Decimal("100.00"), id_categoria)
        id_item = item_repo.inserir(item_catalogo)
        assert id_item is not None
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 200.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        assert id_orcamento is not None
        # Criar 2 item_demandas diferentes para evitar UNIQUE constraint violation
        for i in range(2):
            item_demanda = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, f"Item solicitado {i+1}", 1)
            id_item_demanda = item_demanda_repo.inserir(item_demanda)
            assert id_item_demanda is not None
            item_orc = ItemOrcamento(0, id_orcamento, id_item_demanda, id_item, 1, 100.00, None, None, "PENDENTE")
            item_orcamento_repo.inserir(item_orc)
        # Act
        status = orcamento_repo.calcular_status_derivado(id_orcamento)
        # Assert
        assert status == "PENDENTE", "Todos itens pendentes deveria retornar PENDENTE"

    def test_calcular_status_derivado_parcialmente_aceito(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa cálculo de status derivado com itens mistos - retorna PARCIALMENTE_ACEITO (linhas 167-168)"""
        # Arrange
        usuario_repo.criar_tabela()
        from core.repositories.fornecedor_repo import fornecedor_repo
        fornecedor_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        assert id_demanda is not None
        assert id_fornecedor is not None
        item_catalogo = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste", "Descrição", Decimal("100.00"), id_categoria)
        id_item = item_repo.inserir(item_catalogo)
        assert id_item is not None
        item_demanda = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, "Item solicitado", 1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        assert id_item_demanda is not None
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 300.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        assert id_orcamento is not None
        # Criar 3 item_demandas diferentes para evitar UNIQUE constraint violation
        item_demanda2 = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, "Item solicitado 2", 1)
        item_demanda3 = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, "Item solicitado 3", 1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        id_item_demanda3 = item_demanda_repo.inserir(item_demanda3)
        assert id_item_demanda2 is not None
        assert id_item_demanda3 is not None
        # Criar itens com status mistos: 1 aceito, 1 rejeitado, 1 pendente
        item1 = ItemOrcamento(0, id_orcamento, id_item_demanda, id_item, 1, 100.00, None, None, "ACEITO")
        item2 = ItemOrcamento(0, id_orcamento, id_item_demanda2, id_item, 1, 100.00, None, None, "REJEITADO")
        item3 = ItemOrcamento(0, id_orcamento, id_item_demanda3, id_item, 1, 100.00, None, None, "PENDENTE")
        item_orcamento_repo.inserir(item1)
        item_orcamento_repo.inserir(item2)
        item_orcamento_repo.inserir(item3)
        # Act
        status = orcamento_repo.calcular_status_derivado(id_orcamento)
        # Assert
        assert status == "PARCIALMENTE_ACEITO", "Itens mistos com pelo menos um aceito deveria retornar PARCIALMENTE_ACEITO"

    def test_atualizar_status_derivado(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        """Testa atualização de status derivado (linhas 180-181)"""
        # Arrange
        usuario_repo.criar_tabela()
        from core.repositories.fornecedor_repo import fornecedor_repo
        fornecedor_repo.criar_tabela()
        casal_repo.criar_tabela()
        categoria_repo.criar_tabela()
        demanda_repo.criar_tabela()
        orcamento_repo.criar_tabela()
        item_repo.criar_tabela()
        item_demanda_repo.criar_tabela()
        item_orcamento_repo.criar_tabela()
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir(noivo)
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        casal = Casal(0, 1, 2, None, None, "50k_100k", 100)
        casal_repo.inserir(casal)
        demanda = Demanda(0, 1, "Descrição da demanda de teste")
        id_demanda = demanda_repo.inserir(demanda)
        assert id_demanda is not None
        assert id_fornecedor is not None
        item_catalogo = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste", "Descrição", Decimal("100.00"), id_categoria)
        id_item = item_repo.inserir(item_catalogo)
        assert id_item is not None
        item_demanda = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, "Item solicitado", 1)
        id_item_demanda = item_demanda_repo.inserir(item_demanda)
        assert id_item_demanda is not None
        # Criar 2 item_demandas diferentes para evitar UNIQUE constraint violation
        item_demanda2 = ItemDemanda(0, id_demanda, TipoFornecimento.PRODUTO, id_categoria, "Item solicitado 2", 1)
        id_item_demanda2 = item_demanda_repo.inserir(item_demanda2)
        assert id_item_demanda2 is not None
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, 200.00)
        id_orcamento = orcamento_repo.inserir(orcamento)
        assert id_orcamento is not None
        # Criar 2 itens todos aceitos com item_demandas diferentes
        item_orc1 = ItemOrcamento(0, id_orcamento, id_item_demanda, id_item, 1, 100.00, None, None, "ACEITO")
        item_orc2 = ItemOrcamento(0, id_orcamento, id_item_demanda2, id_item, 1, 100.00, None, None, "ACEITO")
        item_orcamento_repo.inserir(item_orc1)
        item_orcamento_repo.inserir(item_orc2)
        # Act
        sucesso = orcamento_repo.atualizar_status_derivado(id_orcamento)
        # Assert
        assert sucesso is True, "Atualização deveria retornar True"
        orcamento_atualizado = orcamento_repo.obter_por_id(id_orcamento)
        assert orcamento_atualizado.status == "ACEITO", "Status deveria ser atualizado para ACEITO"