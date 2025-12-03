import pytest
from decimal import Decimal
from core.models.item_model import Item
from core.models.categoria_model import Categoria
from core.models.tipo_fornecimento_model import TipoFornecimento
from core.repositories.item_repo import item_repo
from core.repositories.categoria_repo import categoria_repo
from core.repositories.usuario_repo import usuario_repo
from core.repositories.fornecedor_repo import fornecedor_repo
from util.exceptions import RecursoNaoEncontradoError

class TestItemRepo:
    def test_criar_tabela_item(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        # Act
        resultado = item_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_item(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        # Inserir fornecedor e categoria
        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(
            id=0,
            id_fornecedor=id_fornecedor,
            tipo=TipoFornecimento.PRODUTO,
            nome="Item Teste",
            descricao="Descrição do item teste",
            preco=Decimal(99.99),
            id_categoria=id_categoria,
            observacoes="Observações teste",
            ativo=True,
            data_cadastro=None
        )

        # Act
        id_item = item_repo.inserir(item)

        # Assert
        assert id_item is not None, "Deveria retornar o ID do item inserido"
        item_db = item_repo.obter_por_id(id_item)
        assert item_db is not None, "O item inserido não deveria ser None"
        assert item_db.nome == "Item Teste", "O nome do item não confere"
        assert item_db.tipo == TipoFornecimento.PRODUTO, "O tipo do item não confere"
        assert item_db.preco == 99.99, "O preço do item não confere"

    def test_inserir_item_categoria_tipo_incompativel(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        # Criar categoria de PRODUTO
        categoria = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Tentar inserir item de SERVIÇO com categoria de PRODUTO
        item = Item(
            id=0,
            id_fornecedor=id_fornecedor,
            tipo=TipoFornecimento.SERVICO,  # Tipo diferente da categoria
            nome="Item Teste",
            descricao="Descrição do item teste",
            preco=Decimal(99.9),
            id_categoria=id_categoria,
            observacoes=None,
            ativo=True,
            data_cadastro=None
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Categoria .* não pertence ao tipo"):
            item_repo.inserir(item)

    def test_obter_item_por_id_existente(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste",
                   "Descrição", Decimal(50.00), id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Act
        item_db = item_repo.obter_por_id(id_item)

        # Assert
        assert item_db is not None, "O item deveria ser encontrado"
        assert item_db.id == id_item, "O ID do item não confere"
        assert item_db.nome == "Item Teste", "O nome do item não confere"

    def test_obter_item_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            item_repo.obter_por_id(999)

    def test_atualizar_item(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Original",
                   "Descrição Original", Decimal(50.00), id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Atualizar item
        assert id_item is not None
        item_atualizado = Item(id_item, id_fornecedor, TipoFornecimento.PRODUTO,
                              "Item Atualizado", "Nova Descrição", Decimal(75.00),
                              id_categoria, "Novas observações", True, None)

        # Act
        sucesso = item_repo.atualizar(item_atualizado)

        # Assert
        assert sucesso == True, "A atualização deveria ter sucesso"
        item_db = item_repo.obter_por_id(id_item)
        assert item_db.nome == "Item Atualizado", "O nome não foi atualizado"
        assert item_db.descricao == "Nova Descrição", "A descrição não foi atualizada"
        assert item_db.preco == 75.0, "O preço não foi atualizado"

    def test_excluir_item(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste",
                   "Descrição", Decimal(50.00), id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Act
        assert id_item is not None
        sucesso = item_repo.excluir_item_fornecedor(id_item, id_fornecedor)

        # Assert
        assert sucesso == True, "A exclusão deveria ter sucesso"
        with pytest.raises(RecursoNaoEncontradoError):
            item_repo.obter_por_id(id_item)

    def test_obter_itens_por_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir 3 itens para o fornecedor
        for i in range(1, 4):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}",
                       f"Descrição {i}", Decimal(10*i), id_categoria, None, True, None)
            item_repo.inserir(item)

        # Act
        itens = item_repo.obter_itens_por_fornecedor(id_fornecedor)

        # Assert
        assert len(itens) == 3, "Deveria retornar 3 itens"
        assert all(item.id_fornecedor == id_fornecedor for item in itens), "Todos os itens devem ser do fornecedor"
        assert all(item.ativo == True for item in itens), "Todos os itens devem estar ativos"

    def test_obter_itens_por_tipo(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria_produto = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_servico = Categoria(0, "Categoria Serviço", TipoFornecimento.SERVICO, "Descrição", True)
        id_categoria_produto = categoria_repo.inserir(categoria_produto)
        id_categoria_servico = categoria_repo.inserir(categoria_servico)

        # Inserir produtos e serviços
        item_produto = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Produto Teste",
                           "Descrição", Decimal(50.00), id_categoria_produto, None, True, None)
        item_servico = Item(0, id_fornecedor, TipoFornecimento.SERVICO, "Serviço Teste",
                           "Descrição", Decimal(100.00), id_categoria_servico, None, True, None)
        item_repo.inserir(item_produto)
        item_repo.inserir(item_servico)

        # Act
        produtos = item_repo.obter_itens_por_tipo(TipoFornecimento.PRODUTO)
        servicos = item_repo.obter_itens_por_tipo(TipoFornecimento.SERVICO)

        # Assert
        assert len(produtos) == 1, "Deveria retornar 1 produto"
        assert len(servicos) == 1, "Deveria retornar 1 serviço"
        assert produtos[0].tipo == TipoFornecimento.PRODUTO, "Deveria ser um produto"
        assert servicos[0].tipo == TipoFornecimento.SERVICO, "Deveria ser um serviço"

    def test_buscar_itens(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir itens com nomes diferentes
        item1 = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Bolo de Chocolate",
                    "Delicioso bolo", Decimal(50.00), id_categoria, None, True, None)
        item2 = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Torta de Morango",
                    "Torta saborosa", Decimal(60.00), id_categoria, None, True, None)
        item_repo.inserir(item1)
        item_repo.inserir(item2)

        # Act
        resultados_bolo = item_repo.buscar_itens("Bolo")
        resultados_torta = item_repo.buscar_itens("Torta")

        # Assert
        assert len(resultados_bolo) == 1, "Deveria encontrar 1 item com 'Bolo'"
        assert len(resultados_torta) == 1, "Deveria encontrar 1 item com 'Torta'"
        assert resultados_bolo[0].nome == "Bolo de Chocolate", "Deveria encontrar o bolo"
        assert resultados_torta[0].nome == "Torta de Morango", "Deveria encontrar a torta"

    def test_contar_itens_por_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir 5 itens ativos
        for i in range(5):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}",
                       "Descrição", Decimal(50.00), id_categoria, None, True, None)
            item_repo.inserir(item)

        # Act
        total = item_repo.contar_por_fornecedor(id_fornecedor)

        # Assert
        assert total == 5, "Deveria contar 5 itens ativos"

    def test_ativar_desativar_item(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste",
                   "Descrição", Decimal(50.00), id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Act - Desativar
        assert id_item is not None
        sucesso_desativar = item_repo.desativar_item(id_item, id_fornecedor)
        item_desativado = item_repo.obter_por_id(id_item)

        # Act - Ativar
        sucesso_ativar = item_repo.ativar_item(id_item, id_fornecedor)
        item_ativado = item_repo.obter_por_id(id_item)

        # Assert
        assert sucesso_desativar == True, "Desativação deveria ter sucesso"
        assert item_desativado.ativo == False, "Item deveria estar desativado"
        assert sucesso_ativar == True, "Ativação deveria ter sucesso"
        assert item_ativado.ativo == True, "Item deveria estar ativado"

    def test_contar_itens(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir 3 itens
        for i in range(3):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}",
                       "Descrição", Decimal(50.00), id_categoria, None, True, None)
            item_repo.inserir(item)

        # Act
        total = item_repo.contar_itens()

        # Assert
        assert total == 3, "Deveria contar 3 itens no total"

    def test_contar_itens_por_tipo(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria_produto = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_servico = Categoria(0, "Categoria Serviço", TipoFornecimento.SERVICO, "Descrição", True)
        id_categoria_produto = categoria_repo.inserir(categoria_produto)
        id_categoria_servico = categoria_repo.inserir(categoria_servico)

        # Inserir 2 produtos e 1 serviço
        for i in range(2):
            item_produto = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Produto {i}",
                               "Descrição", Decimal(50.00), id_categoria_produto, None, True, None)
            item_repo.inserir(item_produto)

        item_servico = Item(0, id_fornecedor, TipoFornecimento.SERVICO, "Serviço",
                           "Descrição", Decimal(100.00), id_categoria_servico, None, True, None)
        item_repo.inserir(item_servico)

        # Act
        total_produtos = item_repo.contar_itens_por_tipo(TipoFornecimento.PRODUTO)
        total_servicos = item_repo.contar_itens_por_tipo(TipoFornecimento.SERVICO)

        # Assert
        assert total_produtos == 2, "Deveria contar 2 produtos"
        assert total_servicos == 1, "Deveria contar 1 serviço"

    def test_obter_produtos(self, test_db, fornecedor_exemplo):
        """Testa obtenção de produtos ativos (linha 142)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Cat Produto", TipoFornecimento.PRODUTO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Produto", "Desc", Decimal(50), id_categoria, None, True, None)
        item_repo.inserir(item)
        # Act
        produtos = item_repo.obter_produtos()
        # Assert
        assert len(produtos) == 1
        assert produtos[0].tipo == TipoFornecimento.PRODUTO

    def test_obter_servicos(self, test_db, fornecedor_exemplo):
        """Testa obtenção de serviços ativos (linha 146)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Cat Serviço", TipoFornecimento.SERVICO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        item = Item(0, id_fornecedor, TipoFornecimento.SERVICO, "Serviço", "Desc", Decimal(100), id_categoria, None, True, None)
        item_repo.inserir(item)
        # Act
        servicos = item_repo.obter_servicos()
        # Assert
        assert len(servicos) == 1
        assert servicos[0].tipo == TipoFornecimento.SERVICO

    def test_obter_espacos(self, test_db, fornecedor_exemplo):
        """Testa obtenção de espaços ativos (linha 150)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Cat Espaço", TipoFornecimento.ESPACO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        item = Item(0, id_fornecedor, TipoFornecimento.ESPACO, "Espaço", "Desc", Decimal(200), id_categoria, None, True, None)
        item_repo.inserir(item)
        # Act
        espacos = item_repo.obter_espacos()
        # Assert
        assert len(espacos) == 1
        assert espacos[0].tipo == TipoFornecimento.ESPACO

    def test_ativar_desativar_item_admin(self, test_db, fornecedor_exemplo):
        """Testa ativação/desativação admin (linhas 274-275, 279-280)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria", TipoFornecimento.PRODUTO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item", "Desc", Decimal(50), id_categoria, None, True, None)
        id_item = item_repo.inserir(item)
        assert id_item is not None
        # Act
        item_repo.desativar_item_admin(id_item)
        item_desativado = item_repo.obter_por_id(id_item)
        item_repo.ativar_item_admin(id_item)
        item_ativado = item_repo.obter_por_id(id_item)
        # Assert
        assert item_desativado.ativo == False
        assert item_ativado.ativo == True

    def test_atualizar_item_categoria_tipo_incompativel(self, test_db, fornecedor_exemplo):
        """Testa atualização com categoria incompatível (linha 43)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria_produto = Categoria(0, "Cat Produto", TipoFornecimento.PRODUTO, "Desc", True)
        categoria_servico = Categoria(0, "Cat Serviço", TipoFornecimento.SERVICO, "Desc", True)
        id_cat_produto = categoria_repo.inserir(categoria_produto)
        id_cat_servico = categoria_repo.inserir(categoria_servico)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item", "Desc", Decimal(50), id_cat_produto, None, True, None)
        id_item = item_repo.inserir(item)
        assert id_item is not None
        # Act & Assert - Tentar atualizar com categoria incompatível
        item_invalido = Item(id_item, id_fornecedor, TipoFornecimento.SERVICO, "Item", "Desc", Decimal(50), id_cat_produto, None, True, None)
        with pytest.raises(ValueError, match="Categoria .* não pertence ao tipo"):
            item_repo.atualizar(item_invalido)

    def test_obter_itens_por_pagina(self, test_db, fornecedor_exemplo):
        """Testa paginação de itens (linhas 118-119)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria", TipoFornecimento.PRODUTO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        for i in range(5):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}", "Desc", Decimal(50), id_categoria, None, True, None)
            item_repo.inserir(item)
        # Act
        itens_pag1 = item_repo.obter_itens_por_pagina(1, 2)
        itens_pag2 = item_repo.obter_itens_por_pagina(2, 2)
        # Assert
        assert len(itens_pag1) == 2
        assert len(itens_pag2) == 2

    def test_obter_paginado_itens(self, test_db, fornecedor_exemplo):
        """Testa paginação com total (linha 286)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria", TipoFornecimento.PRODUTO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        for i in range(7):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}", "Desc", Decimal(50), id_categoria, None, True, None)
            item_repo.inserir(item)
        # Act
        itens, total = item_repo.obter_paginado_itens(1, 3)
        # Assert
        assert len(itens) == 3
        assert total == 7

    def test_obter_estatisticas_itens(self, test_db, fornecedor_exemplo):
        """Testa estatísticas de itens por tipo (linha 160)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        cat_produto = Categoria(0, "Produto", TipoFornecimento.PRODUTO, "Desc", True)
        id_cat = categoria_repo.inserir(cat_produto)
        assert id_cat is not None

        for i in range(3):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}", "Desc", Decimal(50), id_cat, None, True, None)
            item_repo.inserir(item)
        # Act
        stats = item_repo.obter_estatisticas_itens()
        # Assert
        assert len(stats) > 0
        assert any(s["tipo"] == "PRODUTO" for s in stats)

    def test_obter_itens_ativos_por_categoria(self, test_db, fornecedor_exemplo):
        """Testa obtenção de itens por categoria (linhas 341-344)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        categoria = Categoria(0, "Categoria", TipoFornecimento.PRODUTO, "Desc", True)
        id_categoria = categoria_repo.inserir(categoria)
        assert id_categoria is not None

        for i in range(2):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}", "Desc", Decimal(50), id_categoria, None, True, None)
            item_repo.inserir(item)
        # Act
        itens = item_repo.obter_itens_ativos_por_categoria(id_categoria)
        # Assert
        assert len(itens) == 2
        assert all(isinstance(i, dict) for i in itens)
        assert all(i["id_categoria"] == id_categoria for i in itens if "id_categoria" in i)

    def test_obter_categorias_do_fornecedor(self, test_db, fornecedor_exemplo):
        """Testa obtenção de categorias oferecidas pelo fornecedor (linhas 358-361)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        assert id_fornecedor is not None
        cat1 = Categoria(0, "Cat 1", TipoFornecimento.PRODUTO, "Desc", True)
        cat2 = Categoria(0, "Cat 2", TipoFornecimento.SERVICO, "Desc", True)
        id_cat1 = categoria_repo.inserir(cat1)
        assert id_cat1 is not None
        id_cat2 = categoria_repo.inserir(cat2)
        assert id_cat2 is not None

        item1 = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item 1", "Desc", Decimal(50), id_cat1, None, True, None)
        item2 = Item(0, id_fornecedor, TipoFornecimento.SERVICO, "Item 2", "Desc", Decimal(100), id_cat2, None, True, None)
        item_repo.inserir(item1)
        item_repo.inserir(item2)
        # Act
        categorias = item_repo.obter_categorias_do_fornecedor(id_fornecedor)
        # Assert
        assert len(categorias) == 2
        assert id_cat1 in categorias
        assert id_cat2 in categorias

    def test_validar_categoria_inexistente(self, test_db):
        """Testa validação com categoria inexistente (linha 16)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()
        # Act & Assert - obter_por_id lança exceção quando não encontra
        from core.repositories.item_repo import validar_categoria_para_tipo
        with pytest.raises(RecursoNaoEncontradoError):
            validar_categoria_para_tipo(TipoFornecimento.PRODUTO, 999)