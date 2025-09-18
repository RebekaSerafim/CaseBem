from model.fornecedor_produto_model import FornecedorProduto
from repo import fornecedor_produto_repo, usuario_repo, produto_repo

class TestFornecedorProdutoRepo:
    def test_criar_tabela_fornecedor_produto(self, test_db):
        assert fornecedor_produto_repo.criar_tabela_fornecedor_produto() is True

    def test_inserir_fornecedor_produto(self, test_db, fornecedor_produto_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        
        # Act
        ids = fornecedor_produto_repo.inserir_fornecedor_produto(fornecedor_produto_exemplo)
        
        # Assert
        assert ids == (1, 1)

    def test_atualizar_fornecedor_produto(self, test_db, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        
        fp = Fornecedor(1, 1, "Observações iniciais", 50.0)
        fornecedor_produto_repo.inserir_fornecedor_produto(fp)
        
        # Act
        fp_atualizado = Fornecedor(1, 1, "Observações atualizadas", 75.0)
        sucesso = fornecedor_produto_repo.atualizar_fornecedor_produto(fp_atualizado)
        
        # Assert
        assert sucesso is True
        fp_obtido = fornecedor_produto_repo.obter_fornecedor_produto_por_id(1, 1)
        assert fp_obtido.observacoes == "Observações atualizadas"
        assert fp_obtido.preco == 75.0

    def test_excluir_fornecedor_produto(self, test_db, fornecedor_produto_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        fornecedor_produto_repo.inserir_fornecedor_produto(fornecedor_produto_exemplo)
        
        # Act
        sucesso = fornecedor_produto_repo.excluir_fornecedor_produto(1, 1)
        
        # Assert
        assert sucesso is True
        assert fornecedor_produto_repo.obter_fornecedor_produto_por_id(1, 1) is None

    def test_obter_fornecedor_produto_por_id(self, test_db, fornecedor_produto_exemplo, fornecedor_exemplo, produto_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        produto_repo.inserir_produto(produto_exemplo)
        fornecedor_produto_repo.inserir_fornecedor_produto(fornecedor_produto_exemplo)
        
        # Act
        fp = fornecedor_produto_repo.obter_fornecedor_produto_por_id(1, 1)
        
        # Assert
        assert fp is not None
        assert fp.id_fornecedor == 1
        assert fp.id_produto == 1
        assert fp.observacoes == "Observações teste"
        assert fp.preco == 50.0

    def test_obter_fornecedores_produto_por_pagina(self, test_db, fornecedor_exemplo, lista_produtos_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        produto_repo.criar_tabela_produtos()
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        
        usuario_repo.inserir_usuario(fornecedor_exemplo)
        for produto in lista_produtos_exemplo[:5]:
            produto_repo.inserir_produto(produto)
        
        # Inserir relações
        for i in range(1, 6):
            fp = Fornecedor(1, i, f"Observações {i}", 50.0 * i)
            fornecedor_produto_repo.inserir_fornecedor_produto(fp)
        
        # Act
        pagina = fornecedor_produto_repo.obter_fornecedores_produto_por_pagina(1, 3)
        
        # Assert
        assert len(pagina) == 3
        assert all(isinstance(fp, Fornecedor) for fp in pagina)