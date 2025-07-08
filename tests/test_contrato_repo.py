# #from model.usuario_model import Usuario
# from model.contrato_model import Contrato
# from repo import contrato_repo

# class TestContratoRepo:
#     def test_criar_tabela_contratos(self, test_db):
#         # Arrange
#         # Act
#         resultado = contrato_repo.criar_tabela_contratos()
#         # Assert
#         assert resultado == True, "A criação da tabela deveria retornar True"        

#     def test_inserir_contrato(self, test_db, contrato_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         # Act
#         id_contrato_inserido = contrato_repo.inserir_contrato(contrato_exemplo)
#         # Assert
#         contrato_db = contrato_repo.obter_contrato_por_id(id_contrato_inserido)
#         assert contrato_db is not None, "O contrato inserido não deveria ser None"
#         assert contrato_db.id == 1, "O contrato inserido deveria ter um ID igual a 1"
#         assert contrato_db.nome == "Contrato Teste", "O nome do contrato inserido não confere"
#         assert contrato_db.valor == 1000.0, "O valor do contrato inserido não confere"

#     def test_obter_contrato_por_id_existente(self, test_db, contrato_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()        
#         id_contrato_inserido = contrato_repo.inserir_contrato(contrato_exemplo)
#         # Act
#         contrato_db = contrato_repo.obter_contrato_por_id(id_contrato_inserido)
#         # Assert
#         assert contrato_db is not None, "O contrato inserido não deveria ser None"
#         assert contrato_db.id == 1, "O contrato inserido deveria ter um ID igual a 1"
#         assert contrato_db.nome == "Contrato Teste", "O nome do contrato inserido não confere"
#         assert contrato_db.valor == 1000.0, "O valor do contrato inserido não confere"

#     def test_obter_contrato_por_id_inexistente(self, test_db):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         # Act
#         contrato_db = contrato_repo.obter_contrato_por_id(999)
#         # Assert
#         assert contrato_db is None, "O contrato buscado com ID inexistente deveria retornar None"


#     def test_atualizar_contrato_existente(self, test_db, contrato_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         id_contrato_inserido = contrato_repo.inserir_contrato(contrato_exemplo)
#         contrato_inserido = contrato_repo.obter_contrato_por_id(id_contrato_inserido)
#         # Act
#         contrato_inserido.nome = "Contrato Atualizado"
#         contrato_inserido.valor = 1500.0

#         resultado = contrato_repo.atualizar_contrato(contrato_inserido)
#         # Assert
#         assert resultado == True, "A atualização do contrato deveria retornar True"
#         contrato_db = contrato_repo.obter_contrato_por_id(id_contrato_inserido)
#         assert contrato_db.nome == "Contrato Atualizado", "O nome do contrato atualizado não confere"
#         assert contrato_db.valor == 1500.0, "O valor do contrato atualizado não confere"

#     def test_atualizar_contrato_inexistente(self, test_db, contrato_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         contrato_exemplo.id = 999  # ID que não existe
#         # Act
#         resultado = contrato_repo.atualizar_contrato(contrato_exemplo)
#         # Assert
#         assert resultado == False, "A atualização de um contrato inexistente deveria retornar False"

#     def test_excluir_contrato_existente(self, test_db, contrato_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()        
#         id_contrato_inserido = contrato_repo.inserir_contrato(contrato_exemplo)
#         # Act
#         resultado = contrato_repo.excluir_contrato(id_contrato_inserido)
#         # Assert
#         assert resultado == True, "O resultado da exclusão deveria ser True"
#         contrato_excluido = contrato_repo.obter_contrato_por_id(id_contrato_inserido)
#         assert contrato_excluido is None, "O contrato excluído deveria ser None"

#     def test_excluir_contrato_inexistente(self, test_db):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         # Act
#         resultado = contrato_repo.excluir_contrato(999)
#         # Assert
#         assert resultado == False, "A exclusão de um contrato inexistente deveria retornar False"


#     def test_obter_contratos_por_pagina_primeira_pagina(self, test_db, lista_contratos_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         for contrato in lista_contratos_exemplo:
#             contrato_repo.inserir_contrato(contrato)
#         # Act
#         pagina_contratos = contrato_repo.obter_contratos_por_pagina(1, 4)
#         # Assert
#         assert len(pagina_contratos) == 4, "Deveria retornar 4 contratos na primeira página"
#         assert all(isinstance(u, Contrato) for u in pagina_contratos), "Todos os itens da página devem ser do tipo Contrato"
#         ids_esperados = [1, 2, 3, 4]
#         ids_retornados = [u.id for u in pagina_contratos]
#         assert ids_esperados == ids_retornados, "Os IDs dos contratos na primeira página não estão corretos"
    
#     def test_obter_contratos_por_pagina_terceira_pagina(self, test_db, lista_contratos_exemplo):
#         # Arrange
#         contrato_repo.criar_tabela_contratos()
#         for contrato in lista_contratos_exemplo:
#             contrato_repo.inserir_contrato(contrato)
#         # Act: busca a terceira página com 4 contratos por página
#         pagina_contratos = contrato_repo.obter_contratos_por_pagina(3, 4)
#         # Assert: verifica se retornou a quantidade correta (2 usuários na terceira página)
#         assert len(pagina_contratos) == 2, "Deveria retornar 2 usuários na terceira página"
#         assert (isinstance(c, Contrato) for c in pagina_contratos), "Todos os itens da página devem ser do tipo Usuario"