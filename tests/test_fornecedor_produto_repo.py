from model.fornecedor_produto_model import FornecedorProduto
from repo import fornecedor_produto_repo

class TestFornecedorProdutoRepo:
    def test_criar_tabela_fornecedor_produto(self, test_db):
        assert fornecedor_produto_repo.criar_tabela_fornecedor_produto() is True

    def test_inserir_fornecedor_produto(self, test_db, relacao_exemplo):
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        sucesso = fornecedor_produto_repo.inserir_relacao(relacao_exemplo)
        assert sucesso is True

    def test_excluir_fornecedor_produto(self, test_db, relacao_exemplo):
        fornecedor_produto_repo.criar_tabela_fornecedor_produto()
        fornecedor_produto_repo.inserir_relacao(relacao_exemplo)
        assert fornecedor_produto_repo.excluir_relacao(relacao_exemplo.idFornecedor, relacao_exemplo.idProduto) is True