from model.produto_model import Produto
from repo import produto_repo

class TestProdutoRepo:
    def test_criar_tabela_produtos(self, test_db):
        # Arrange
        # Act
        resultado = produto_repo.criar_tabela_produtos()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_produto(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Assert
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db is not None, "O produto inserido não deveria ser None"
        assert produto_db.id == 1, "O produto inserido deveria ter um ID igual a 1"
        assert produto_db.nome == "Produto Teste", "O nome do produto inserido não confere"
        assert produto_db.preco == "19.99", "O preço do produto inserido não confere"
        assert produto_db.quantidade == "10", "A quantidade do produto inserido não confere"
        assert produto_db.descricao == "Descrição do produto teste", "A descrição do produto inserido não confere"

    def test_obter_produto_por_id_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()        
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        # Assert
        assert produto_db is not None, "O produto retornado deveria ser diferente de None"
        assert produto_db.id == id_produto_inserido, "O id do produto buscado deveria ser igual ao id do produto inserido"
        assert produto_db.nome == produto_exemplo.nome, "O nome do produto buscado deveria ser igual ao nome do produto inserido"
        assert produto_db.preco == produto_exemplo.preco, "O preço do produto buscado deveria ser igual ao preço do produto inserido"
        assert produto_db.quantidade == produto_exemplo.quantidade, "A quantidade do produto buscado deveria ser igual à quantidade do produto inserida"
        assert produto_db.descricao == produto_exemplo.descricao, "A descrição do produto buscado deveria ser igual à descrição do produto inserido"

    def test_obter_produto_por_id_inexistente(self, test_db):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        produto_db = produto_repo.obter_produto_por_id(999)
        # Assert
        assert produto_db is None, "O produto buscado com ID inexistente deveria retornar None"

    def test_obter_produto_por_nome_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        produto_db = produto_repo.obter_produto_por_nome(produto_exemplo.nome)
        # Assert
        assert produto_db is not None, "O produto buscado por nome deveria ser diferente de None"
        assert produto_db.id == id_produto_inserido, "O id do produto buscado por nome deveria ser igual ao id do produto inserido"
        assert produto_db.nome == produto_exemplo.nome, "O nome do produto buscado deveria ser igual ao nome do produto inserido"

    def test_obter_produto_por_nome_inexistente(self, test_db):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        produto_db = produto_repo.obter_produto_por_nome("Produto Inexistente")
        # Assert
        assert produto_db is None, "O produto buscado por nome inexistente deveria retornar None"

    def test_atualizar_produto_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        produto_inserido = produto_repo.obter_produto_por_id(id_produto_inserido)
        # Act
        produto_inserido.nome = "Produto Atualizado"
        produto_inserido.preco = "20.99"
        produto_inserido.quantidade = "15"
        produto_inserido.descricao = "Descrição do produto atualizado"
        resultado = produto_repo.atualizar_produto(produto_inserido)
        # Assert
        assert resultado == True, "A atualização do produto deveria retornar True"
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db.nome == "Produto Atualizado", "O nome do produto atualizado não confere"
        assert produto_db.preco == "20.99", "O preço do produto atualizado não confere"
        assert produto_db.quantidade == "15", "A quantidade do produto atualizado não confere"
        assert produto_db.descricao == "Descrição do produto atualizado", "A descrição atualizada não confere"

    def test_atualizar_produto_inexistente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        produto_exemplo.id = 999  # ID que não existe
        # Act
        resultado = produto_repo.atualizar_produto(produto_exemplo)
        # Assert
        assert resultado == False, "A atualização de um produto inexistente deveria retornar False"

    def test_excluir_produto_existente(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()        
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        resultado = produto_repo.excluir_produto(id_produto_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        produto_excluido = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_excluido is None, "O produto excluído deveria ser None"

    def test_excluir_produto_inexistente(self, test_db):
        # Arrange
        produto_repo.criar_tabela_produtos()
        # Act
        resultado = produto_repo.excluir_produto(999)
        # Assert
        assert resultado == False, "A exclusão de um produto inexistente deveria retornar False"

    def test_atualizar_tipo_produto(self, test_db, produto_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        id_produto_inserido = produto_repo.inserir_produto(produto_exemplo)
        # Act
        resultado = produto_repo.atualizar_tipo_produto(id_produto_inserido, 1)
        # Assert
        assert resultado == True, "A atualização do tipo de produto deveria retornar True"
        produto_db = produto_repo.obter_produto_por_id(id_produto_inserido)
        assert produto_db.tipo == 1, "O tipo do produto atualizado não confere"

    def test_obter_produtos_por_pagina_primeira_pagina(self, test_db, lista_produtos_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        for produto in lista_produtos_exemplo:
            produto_repo.inserir_produto(produto)
        # Act
        pagina_produtos = produto_repo.obter_produtos_por_pagina(1, 4)
        # Assert
        assert len(pagina_produtos) == 4, "Deveria retornar 4 produtos na primeira página"
        assert all(isinstance(u, Produto) for u in pagina_produtos), "Todos os itens da página devem ser do tipo Produto"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_produtos]
        assert ids_esperados == ids_retornados, "Os IDs dos produtos na primeira página não estão corretos"
    
    def test_obter_produtos_por_pagina_terceira_pagina(self, test_db, lista_produtos_exemplo):
        # Arrange
        produto_repo.criar_tabela_produtos()
        for produto in lista_produtos_exemplo:
            produto_repo.inserir_produto(produto)
        # Act: busca a terceira página com 4 produtos por página
        pagina_produtos = produto_repo.obter_produtos_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 produtos na terceira página)
        assert len(pagina_produtos) == 2, "Deveria retornar 2 produtos na terceira página"
        assert (isinstance(u, Produto) for u in pagina_produtos), "Todos os itens da página devem ser do tipo Produto"