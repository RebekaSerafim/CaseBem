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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(
            id=0,
            id_fornecedor=id_fornecedor,
            tipo=TipoFornecimento.PRODUTO,
            nome="Item Teste",
            descricao="Descrição do item teste",
            preco=99.99,
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
            preco=99.99,
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste",
                   "Descrição", 50.00, id_categoria, None, True, None)
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Original",
                   "Descrição Original", 50.00, id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Atualizar item
        item_atualizado = Item(id_item, id_fornecedor, TipoFornecimento.PRODUTO,
                              "Item Atualizado", "Nova Descrição", 75.00,
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste",
                   "Descrição", 50.00, id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Act
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir 3 itens para o fornecedor
        for i in range(1, 4):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}",
                       f"Descrição {i}", float(10*i), id_categoria, None, True, None)
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
        categoria_produto = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_servico = Categoria(0, "Categoria Serviço", TipoFornecimento.SERVICO, "Descrição", True)
        id_categoria_produto = categoria_repo.inserir(categoria_produto)
        id_categoria_servico = categoria_repo.inserir(categoria_servico)

        # Inserir produtos e serviços
        item_produto = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Produto Teste",
                           "Descrição", 50.00, id_categoria_produto, None, True, None)
        item_servico = Item(0, id_fornecedor, TipoFornecimento.SERVICO, "Serviço Teste",
                           "Descrição", 100.00, id_categoria_servico, None, True, None)
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir itens com nomes diferentes
        item1 = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Bolo de Chocolate",
                    "Delicioso bolo", 50.00, id_categoria, None, True, None)
        item2 = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Torta de Morango",
                    "Torta saborosa", 60.00, id_categoria, None, True, None)
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir 5 itens ativos
        for i in range(5):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}",
                       "Descrição", 50.00, id_categoria, None, True, None)
            item_repo.inserir(item)

        # Act
        total = item_repo.contar_itens_por_fornecedor(id_fornecedor)

        # Assert
        assert total == 5, "Deveria contar 5 itens ativos"

    def test_ativar_desativar_item(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        categoria_repo.criar_tabela()
        item_repo.criar_tabela()

        id_fornecedor = fornecedor_repo.inserir(fornecedor_exemplo)
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, "Item Teste",
                   "Descrição", 50.00, id_categoria, None, True, None)
        id_item = item_repo.inserir(item)

        # Act - Desativar
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
        categoria = Categoria(0, "Categoria Teste", TipoFornecimento.PRODUTO, "Descrição", True)
        id_categoria = categoria_repo.inserir(categoria)

        # Inserir 3 itens
        for i in range(3):
            item = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Item {i}",
                       "Descrição", 50.00, id_categoria, None, True, None)
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
        categoria_produto = Categoria(0, "Categoria Produto", TipoFornecimento.PRODUTO, "Descrição", True)
        categoria_servico = Categoria(0, "Categoria Serviço", TipoFornecimento.SERVICO, "Descrição", True)
        id_categoria_produto = categoria_repo.inserir(categoria_produto)
        id_categoria_servico = categoria_repo.inserir(categoria_servico)

        # Inserir 2 produtos e 1 serviço
        for i in range(2):
            item_produto = Item(0, id_fornecedor, TipoFornecimento.PRODUTO, f"Produto {i}",
                               "Descrição", 50.00, id_categoria_produto, None, True, None)
            item_repo.inserir(item_produto)

        item_servico = Item(0, id_fornecedor, TipoFornecimento.SERVICO, "Serviço",
                           "Descrição", 100.00, id_categoria_servico, None, True, None)
        item_repo.inserir(item_servico)

        # Act
        total_produtos = item_repo.contar_itens_por_tipo(TipoFornecimento.PRODUTO)
        total_servicos = item_repo.contar_itens_por_tipo(TipoFornecimento.SERVICO)

        # Assert
        assert total_produtos == 2, "Deveria contar 2 produtos"
        assert total_servicos == 1, "Deveria contar 1 serviço"