# from model.item_contrato_produto_model import ItemContratoProduto
# from repo import item_contrato_produto_repo

# class TestItemContratoProdutoRepo:
#     def test_criar_tabela(self, test_db):
#         assert item_contrato_produto_repo.criar_tabela() == True

#     def test_inserir_item(self, test_db, item_exemplo):
#         id_item = item_contrato_produto_repo.inserir(item_exemplo)
#         item = item_contrato_produto_repo.obter_por_id(id_item)
#         assert item.id == id_item

#     def test_atualizar_item(self, test_db, item_exemplo):
#         id_item = item_contrato_produto_repo.inserir(item_exemplo)
#         item = item_contrato_produto_repo.obter_por_id(id_item)
#         item.quantidade = 999
#         assert item_contrato_produto_repo.atualizar(item) == True

#     def test_excluir_item(self, test_db, item_exemplo):
#         id_item = item_contrato_produto_repo.inserir(item_exemplo)
#         assert item_contrato_produto_repo.excluir(id_item) == True

#     def test_obter_inexistente(self, test_db):
#         assert item_contrato_produto_repo.obter_por_id(9999) is None
