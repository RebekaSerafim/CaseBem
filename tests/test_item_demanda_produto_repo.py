from datetime import datetime
from model.item_demanda_produto_model import ItemDemandaProduto
from model.demanda_model import Demanda
from model.casal_model import Casal
from repo import item_demanda_produto_repo, demanda_repo, produto_repo, casal_repo, usuario_repo

class TestItemDemandaProdutoRepo:
    def test_criar_tabela_item_demanda_produto(self, test_db):
        assert item_demanda_produto_repo.criar_tabela_item_demanda_produto() is True

    def test_inserir_item_demanda_produto(self, test_db, item_demanda_produto_exemplo, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        # Inserir dados necessários
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        # Act
        sucesso = item_demanda_produto_repo.inserir_item_demanda_produto(item_demanda_produto_exemplo)
        
        # Assert
        assert sucesso is True

    def test_obter_item_demanda_produto_por_id(self, test_db, item_demanda_produto_exemplo, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        item_demanda_produto_repo.inserir_item_demanda_produto(item_demanda_produto_exemplo)
        
        # Act
        item = item_demanda_produto_repo.obter_item_demanda_produto_por_id(1, 1)
        
        # Assert
        assert item is not None
        assert item.id_demanda == 1
        assert item.id_produto == 1
        assert item.quantidade == 2
        assert item.observacoes == "Observações do item"

    def test_atualizar_item_demanda_produto(self, test_db, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        item = ItemDemandaProduto(1, 1, 2, "Observações iniciais")
        item_demanda_produto_repo.inserir_item_demanda_produto(item)
        
        # Act
        item_atualizado = ItemDemandaProduto(1, 1, 5, "Observações atualizadas")
        sucesso = item_demanda_produto_repo.atualizar_item_demanda_produto(item_atualizado)
        
        # Assert
        assert sucesso is True
        item_obtido = item_demanda_produto_repo.obter_item_demanda_produto_por_id(1, 1)
        assert item_obtido.quantidade == 5
        assert item_obtido.observacoes == "Observações atualizadas"

    def test_excluir_item_demanda_produto(self, test_db, item_demanda_produto_exemplo, lista_noivos_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        produto_repo.inserir_produto(produto_exemplo)
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        item_demanda_produto_repo.inserir_item_demanda_produto(item_demanda_produto_exemplo)
        
        # Act
        sucesso = item_demanda_produto_repo.excluir_item_demanda_produto(1, 1)
        
        # Assert
        assert sucesso is True
        assert item_demanda_produto_repo.obter_item_demanda_produto_por_id(1, 1) is None

    def test_obter_itens_por_demanda(self, test_db, lista_noivos_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        for noivo in lista_noivos_exemplo[:2]:
            usuario_repo.inserir_usuario(noivo)
        casal = Casal(0, 1, 2, 10000.0)
        casal_repo.inserir_casal(casal)
        
        for produto in lista_produtos_exemplo[:3]:
            produto_repo.inserir_produto(produto)
        
        demanda = Demanda(0, 1, datetime.now())
        demanda_repo.inserir_demanda(demanda)
        
        # Inserir itens
        for i in range(1, 4):
            item = ItemDemandaProduto(1, i, i * 2, f"Observações {i}")
            item_demanda_produto_repo.inserir_item_demanda_produto(item)
        
        # Act
        itens = item_demanda_produto_repo.obter_itens_por_demanda(1)
        
        # Assert
        assert len(itens) == 3
        assert all(isinstance(item, ItemDemandaProduto) for item in itens)
        assert all(item.id_demanda == 1 for item in itens)

    def test_obter_itens_demanda_produto_por_pagina(self, test_db, lista_noivos_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        casal_repo.criar_tabela_casal()
        produto_repo.criar_tabela_produtos()
        demanda_repo.criar_tabela_demandas()
        item_demanda_produto_repo.criar_tabela_item_demanda_produto()
        
        # Inserir usuários e casais
        for usuario in lista_noivos_exemplo[:4]:
            usuario_repo.inserir_usuario(usuario)
        casal1 = Casal(0, 1, 2, 10000.0)
        casal2 = Casal(0, 3, 4, 15000.0)
        casal_repo.inserir_casal(casal1)
        casal_repo.inserir_casal(casal2)
        
        # Inserir produtos
        for produto in lista_produtos_exemplo[:5]:
            produto_repo.inserir_produto(produto)
        
        # Inserir demandas
        demanda1 = Demanda(0, 1, datetime.now())
        demanda2 = Demanda(0, 2, datetime.now())
        demanda_repo.inserir_demanda(demanda1)
        demanda_repo.inserir_demanda(demanda2)
        
        # Inserir itens
        for d in range(1, 3):
            for p in range(1, 4):
                item = ItemDemandaProduto(d, p, p, f"Obs {d}-{p}")
                item_demanda_produto_repo.inserir_item_demanda_produto(item)
        
        # Act
        pagina = item_demanda_produto_repo.obter_itens_demanda_produto_por_pagina(1, 4)
        
        # Assert
        assert len(pagina) == 4
        assert all(isinstance(item, ItemDemandaProduto) for item in pagina)