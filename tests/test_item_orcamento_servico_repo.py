from datetime import datetime
from model.orcamento_model import Orcamento
from model.demanda_model import Demanda
from model.casal_model import Casal
from model.item_orcamento_servico_model import ItemOrcamentoServico
from repo import item_orcamento_servico_repo, orcamento_repo, demanda_repo, casal_repo, usuario_repo, servico_repo

class TestItemOrcamentoServicoRepo:
    def test_criar_tabela_item_orcamento_servico(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        # Agora criar tabela item_orcamento_servico
        assert item_orcamento_servico_repo.criar_tabela_item_orcamento_servico() is True

    def test_inserir_item_orcamento_servico(self, test_db, lista_noivos_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_servico = servico_repo.inserir_servico(servico_exemplo)
        
        # Criar item
        item = ItemOrcamentoServico(
            id_orcamento=id_orcamento,
            id_servico=id_servico,
            preco_unitario=150.00,
            quantidade=2,
            observacoes="Serviço de teste"
        )
        
        # Act
        sucesso = item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Assert
        assert sucesso is True
        item_salvo = item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(id_orcamento, id_servico)
        assert item_salvo is not None
        assert item_salvo.preco_unitario == 150.00
        assert item_salvo.quantidade == 2
        assert item_salvo.observacoes == "Serviço de teste"

    def test_atualizar_item_orcamento_servico(self, test_db, lista_noivos_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_servico = servico_repo.inserir_servico(servico_exemplo)
        
        item = ItemOrcamentoServico(id_orcamento, id_servico, 150.00, 2, "Serviço inicial")
        item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        item.preco_unitario = 200.00
        item.quantidade = 3
        item.observacoes = "Serviço atualizado"
        sucesso = item_orcamento_servico_repo.atualizar_item_orcamento_servico(item)
        
        # Assert
        assert sucesso is True
        item_verificado = item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(id_orcamento, id_servico)
        assert item_verificado.preco_unitario == 200.00
        assert item_verificado.quantidade == 3
        assert item_verificado.observacoes == "Serviço atualizado"

    def test_excluir_item_orcamento_servico(self, test_db, lista_noivos_exemplo, prestador_exemplo, servico_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_servico = servico_repo.inserir_servico(servico_exemplo)
        
        item = ItemOrcamentoServico(id_orcamento, id_servico, 150.00, 2, None)
        item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        sucesso = item_orcamento_servico_repo.excluir_item_orcamento_servico(id_orcamento, id_servico)
        
        # Assert
        assert sucesso is True
        assert item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(id_orcamento, id_servico) is None

    def test_obter_item_orcamento_servico_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        # Act
        item = item_orcamento_servico_repo.obter_item_orcamento_servico_por_id(999, 999)
        
        # Assert
        assert item is None

    def test_obter_itens_por_orcamento(self, test_db, lista_noivos_exemplo, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir serviços e itens
        for i, servico in enumerate(lista_servicos_exemplo[:3]):
            id_servico = servico_repo.inserir_servico(servico)
            item = ItemOrcamentoServico(id_orcamento, id_servico, 100.0 * (i+1), i+1, f"Serviço {i+1}")
            item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        itens = item_orcamento_servico_repo.obter_itens_por_orcamento(id_orcamento)
        
        # Assert
        assert len(itens) == 3
        assert all(item.id_orcamento == id_orcamento for item in itens)
        assert itens[0].preco_unitario == 100.0
        assert itens[1].preco_unitario == 200.0
        assert itens[2].preco_unitario == 300.0

    def test_obter_itens_orcamento_servico_por_pagina(self, test_db, lista_noivos_exemplo, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Criar múltiplos orçamentos e itens
        ids_orcamentos = []
        for i in range(3):
            demanda = Demanda(0, 1, datetime.now())
            id_demanda = demanda_repo.inserir_demanda(demanda)
            orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
            ids_orcamentos.append(orcamento_repo.inserir_orcamento(orcamento))
        
        # Inserir serviços e itens
        for servico in lista_servicos_exemplo[:3]:
            id_servico = servico_repo.inserir_servico(servico)
            for id_orcamento in ids_orcamentos:
                item = ItemOrcamentoServico(id_orcamento, id_servico, 100.0, 1, None)
                item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act - Total de 9 itens (3 orçamentos x 3 serviços)
        pagina1 = item_orcamento_servico_repo.obter_itens_orcamento_servico_por_pagina(1, 5)
        pagina2 = item_orcamento_servico_repo.obter_itens_orcamento_servico_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 4
        assert all(isinstance(item, ItemOrcamentoServico) for item in pagina1)
        assert all(isinstance(item, ItemOrcamentoServico) for item in pagina2)

    def test_calcular_total_itens_servico_orcamento(self, test_db, lista_noivos_exemplo, prestador_exemplo, lista_servicos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir serviços e itens com valores conhecidos
        servicos_precos = [(100.0, 2), (250.0, 1), (500.0, 1)]  # (preco_unitario, quantidade)
        for i, (servico, (preco, qtd)) in enumerate(zip(lista_servicos_exemplo[:3], servicos_precos)):
            id_servico = servico_repo.inserir_servico(servico)
            item = ItemOrcamentoServico(id_orcamento, id_servico, preco, qtd, None)
            item_orcamento_servico_repo.inserir_item_orcamento_servico(item)
        
        # Act
        total = item_orcamento_servico_repo.calcular_total_itens_servico_orcamento(id_orcamento)
        
        # Assert
        # Total = (100*2) + (250*1) + (500*1) = 200 + 250 + 500 = 950
        assert total == 950.0

    def test_calcular_total_itens_servico_orcamento_vazio(self, test_db, lista_noivos_exemplo, prestador_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        servico_repo.criar_tabela_servicos()
        item_orcamento_servico_repo.criar_tabela_item_orcamento_servico()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_prestador = usuario_repo.inserir_usuario(prestador_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_prestador, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act - Orçamento sem itens
        total = item_orcamento_servico_repo.calcular_total_itens_servico_orcamento(id_orcamento)
        
        # Assert
        assert total == 0.0