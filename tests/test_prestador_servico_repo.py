
# from model.prestador_servico_model import PrestadorServico
# from repo import prestador_servico_repo

# class TestPrestadorServicoRepo:
#     def test_criar_tabela_prestadores(self, test_db):
#         assert prestador_servico_repo.criar_tabela_prestadores() == True

#     def test_inserir_prestador(self, test_db, prestador_exemplo):
#         id_inserido = prestador_servico_repo.inserir_prestador(prestador_exemplo)
#         prestador = prestador_servico_repo.obter_prestador_por_id(id_inserido)
#         assert prestador.id == id_inserido

#     def test_obter_prestador_por_id_inexistente(self, test_db):
#         assert prestador_servico_repo.obter_prestador_por_id(999) is None

#     def test_atualizar_prestador_existente(self, test_db, prestador_exemplo):
#         id_inserido = prestador_servico_repo.inserir_prestador(prestador_exemplo)
#         prestador = prestador_servico_repo.obter_prestador_por_id(id_inserido)
#         prestador.nome = "Atualizado"
#         assert prestador_servico_repo.atualizar_prestador(prestador) == True

#     def test_atualizar_prestador_inexistente(self, test_db, prestador_exemplo):
#         prestador_exemplo.id = 999
#         assert prestador_servico_repo.atualizar_prestador(prestador_exemplo) == False

#     def test_excluir_prestador_existente(self, test_db, prestador_exemplo):
#         id_inserido = prestador_servico_repo.inserir_prestador(prestador_exemplo)
#         assert prestador_servico_repo.excluir_prestador(id_inserido) == True

#     def test_excluir_prestador_inexistente(self, test_db):
#         assert prestador_servico_repo.excluir_prestador(999) == False

#     def test_obter_prestadores_por_pagina(self, test_db, lista_prestadores):
#         for p in lista_prestadores:
#             prestador_servico_repo.inserir_prestador(p)
#         pagina = prestador_servico_repo.obter_prestadores_por_pagina(1, 2)
#         assert all(isinstance(p, PrestadorServico) for p in pagina)
