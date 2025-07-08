from datetime import datetime
from model.orcamento_model import Orcamento
from model.demanda_model import Demanda
from model.casal_model import Casal
from model.item_orcamento_produto_model import ItemOrcamentoProduto
from repo import item_orcamento_produto_repo, orcamento_repo, demanda_repo, casal_repo, usuario_repo, produto_repo

class TestItemOrcamentoProdutoRepo:
    def test_criar_tabela_item_orcamento_produto(self, test_db):
        # Criar tabelas dependentes primeiro
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        # Agora criar tabela item_orcamento_produto
        assert item_orcamento_produto_repo.criar_tabela_item_orcamento_produto() is True

    def test_inserir_item_orcamento_produto(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_produto = produto_repo.inserir_produto(produto_exemplo)
        
        # Criar item
        item = ItemOrcamentoProduto(
            id_orcamento=id_orcamento,
            id_produto=id_produto,
            preco_unitario=25.50,
            quantidade=3,
            observacoes="Item de teste"
        )
        
        # Act
        sucesso = item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Assert
        assert sucesso is True
        item_salvo = item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(id_orcamento, id_produto)
        assert item_salvo is not None
        assert item_salvo.preco_unitario == 25.50
        assert item_salvo.quantidade == 3
        assert item_salvo.observacoes == "Item de teste"

    def test_atualizar_item_orcamento_produto(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_produto = produto_repo.inserir_produto(produto_exemplo)
        
        item = ItemOrcamentoProduto(id_orcamento, id_produto, 25.50, 3, "Item inicial")
        item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        item.preco_unitario = 30.00
        item.quantidade = 5
        item.observacoes = "Item atualizado"
        sucesso = item_orcamento_produto_repo.atualizar_item_orcamento_produto(item)
        
        # Assert
        assert sucesso is True
        item_verificado = item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(id_orcamento, id_produto)
        assert item_verificado.preco_unitario == 30.00
        assert item_verificado.quantidade == 5
        assert item_verificado.observacoes == "Item atualizado"

    def test_excluir_item_orcamento_produto(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        id_produto = produto_repo.inserir_produto(produto_exemplo)
        
        item = ItemOrcamentoProduto(id_orcamento, id_produto, 25.50, 3, None)
        item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        sucesso = item_orcamento_produto_repo.excluir_item_orcamento_produto(id_orcamento, id_produto)
        
        # Assert
        assert sucesso is True
        assert item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(id_orcamento, id_produto) is None

    def test_obter_item_orcamento_produto_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        # Act
        item = item_orcamento_produto_repo.obter_item_orcamento_produto_por_id(999, 999)
        
        # Assert
        assert item is None

    def test_obter_itens_por_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir produtos e itens
        for i, produto in enumerate(lista_produtos_exemplo[:3]):
            id_produto = produto_repo.inserir_produto(produto)
            item = ItemOrcamentoProduto(id_orcamento, id_produto, 10.0 * (i+1), i+1, f"Item {i+1}")
            item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        itens = item_orcamento_produto_repo.obter_itens_por_orcamento(id_orcamento)
        
        # Assert
        assert len(itens) == 3
        assert all(item.id_orcamento == id_orcamento for item in itens)
        assert itens[0].preco_unitario == 10.0
        assert itens[1].preco_unitario == 20.0
        assert itens[2].preco_unitario == 30.0

    def test_obter_itens_orcamento_produto_por_pagina(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        # Criar múltiplos orçamentos e itens
        ids_orcamentos = []
        for i in range(3):
            demanda = Demanda(0, 1, datetime.now())
            id_demanda = demanda_repo.inserir_demanda(demanda)
            orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
            ids_orcamentos.append(orcamento_repo.inserir_orcamento(orcamento))
        
        # Inserir produtos e itens
        for produto in lista_produtos_exemplo[:3]:
            id_produto = produto_repo.inserir_produto(produto)
            for id_orcamento in ids_orcamentos:
                item = ItemOrcamentoProduto(id_orcamento, id_produto, 10.0, 1, None)
                item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act - Total de 9 itens (3 orçamentos x 3 produtos)
        pagina1 = item_orcamento_produto_repo.obter_itens_orcamento_produto_por_pagina(1, 5)
        pagina2 = item_orcamento_produto_repo.obter_itens_orcamento_produto_por_pagina(2, 5)
        
        # Assert
        assert len(pagina1) == 5
        assert len(pagina2) == 4
        assert all(isinstance(item, ItemOrcamentoProduto) for item in pagina1)
        assert all(isinstance(item, ItemOrcamentoProduto) for item in pagina2)

    def test_calcular_total_itens_produto_orcamento(self, test_db, lista_noivos_exemplo, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Inserir produtos e itens com valores conhecidos
        produtos_precos = [(10.0, 2), (25.0, 3), (100.0, 1)]  # (preco_unitario, quantidade)
        for i, (produto, (preco, qtd)) in enumerate(zip(lista_produtos_exemplo[:3], produtos_precos)):
            id_produto = produto_repo.inserir_produto(produto)
            item = ItemOrcamentoProduto(id_orcamento, id_produto, preco, qtd, None)
            item_orcamento_produto_repo.inserir_item_orcamento_produto(item)
        
        # Act
        total = item_orcamento_produto_repo.calcular_total_itens_produto_orcamento(id_orcamento)
        
        # Assert
        # Total = (10*2) + (25*3) + (100*1) = 20 + 75 + 100 = 195
        assert total == 195.0

    def test_calcular_total_itens_produto_orcamento_vazio(self, test_db, lista_noivos_exemplo, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        demanda_repo.criar_tabela_demandas()
        orcamento_repo.criar_tabela_orcamento()
        produto_repo.criar_tabela_produtos()
        item_orcamento_produto_repo.criar_tabela_item_orcamento_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor_exemplo)
        
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        demanda = Demanda(0, 1, datetime.now())
        id_demanda = demanda_repo.inserir_demanda(demanda)
        
        orcamento = Orcamento(0, id_demanda, id_fornecedor, datetime.now(), None, "PENDENTE", None, None)
        id_orcamento = orcamento_repo.inserir_orcamento(orcamento)
        
        # Act - Orçamento sem itens
        total = item_orcamento_produto_repo.calcular_total_itens_produto_orcamento(id_orcamento)
        
        # Assert
        assert total == 0.0