from model.usuario_model import Usuario
from model.prestador_model import Prestador
from repo import prestador_repo, usuario_repo

class TestPrestadorRepo:
    def test_criar_tabela_prestadores(self, test_db):
        # Arrange
        # Act
        resultado = prestador_repo.criar_tabela_prestadores()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"        

    def test_inserir_prestador(self, test_db, prestador_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        # Act
        id_prestador_inserido = prestador_repo.inserir_prestador(prestador_exemplo)
        # Assert
        prestador_db = prestador_repo.obter_prestador_por_id(id_prestador_inserido)
        assert prestador_db is not None, "O prestador inserido não deveria ser None"
        assert prestador_db.id == 1, "O prestador inserido deveria ter um ID igual a 1"
        assert prestador_db.nome == "Prestador Teste", "O nome do prestador inserido não confere"
        assert prestador_db.telefone == "(28) 99999-0000", "O telefone do prestador inserido não confere"
        assert prestador_db.email == "prestador@email.com", "O email do prestador inserido não confere"
        assert prestador_db.senha_hash == "123456", "A senha hash do prestador inserido não confere"
        assert prestador_db.tipo == "PRESTADOR", "O tipo do prestador inserido não confere"
        assert prestador_db.tipo_pessoa == "FISICA", "O tipo de pessoa do prestador inserido não confere"
        assert prestador_db.documento == "123.456.789-00", "O documento do prestador inserido não confere"

    def test_obter_prestador_por_id_existente(self, test_db, prestador_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        id_prestador_inserido = prestador_repo.inserir_prestador(prestador_exemplo)
        # Act
        prestador_db = prestador_repo.obter_prestador_por_id(id_prestador_inserido)
        # Assert
        assert prestador_db is not None, "O prestador retornado deveria ser diferente de None"
        assert prestador_db.id == id_prestador_inserido, "O id do prestador buscado deveria ser igual ao id do prestador inserido"
        assert prestador_db.nome == prestador_exemplo.nome, "O nome do prestador buscado deveria ser igual ao nome do prestador inserido"
        assert prestador_db.telefone == prestador_exemplo.telefone, "O telefone do prestador buscado deveria ser igual ao telefone do prestador inserido"
        assert prestador_db.email == prestador_exemplo.email, "O email do prestador buscado deveria ser igual ao email do prestador inserido"
        assert prestador_db.senha_hash == prestador_exemplo.senha_hash, "A senha hash do prestador buscado deveria ser igual à senha hash do prestador inserido"
        assert prestador_db.tipo == prestador_exemplo.tipo, "O tipo do prestador buscado deveria ser igual ao tipo do prestador inserido"
        assert prestador_db.tipo_pessoa == "FISICA", "O tipo de pessoa do prestador inserido não confere"
        assert prestador_db.documento == "123.456.789-00", "O documento do prestador inserido não confere"

    def test_obter_prestador_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        # Act
        prestador_db = prestador_repo.obter_prestador_por_id(999)
        # Assert
        assert prestador_db is None, "O prestador buscado com ID inexistente deveria retornar None"

    def test_obter_usuario_por_email_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        id_usuario_inserido = prestador_repo.inserir_usuario(usuario_exemplo)
        # Act
        usuario_db = prestador_repo.obter_usuario_por_email(usuario_exemplo.email)
        # Assert
        assert usuario_db is not None, "O usuário buscado por email deveria ser diferente de None"
        assert usuario_db.id == id_usuario_inserido, "O id do usuário buscado por email deveria ser igual ao id do usuário inserido"
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário buscado deveria ser igual ao email do usuário inserido"

    def test_obter_usuario_por_email_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        # Act
        usuario_db = prestador_repo.obter_usuario_por_email("inexistente@email.com")
        # Assert
        assert usuario_db is None, "O usuário buscado por email inexistente deveria retornar None"

    def test_atualizar_usuario_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        id_usuario_inserido = prestador_repo.inserir_usuario(usuario_exemplo)
        usuario_inserido = prestador_repo.obter_usuario_por_id(id_usuario_inserido)
        # Act
        usuario_inserido.nome = "Usuário Atualizado"
        usuario_inserido.telefone = "(28) 88888-0000"
        usuario_inserido.email = "usuario_atualizado@email.com"
        resultado = prestador_repo.atualizar_usuario(usuario_inserido)
        # Assert
        assert resultado == True, "A atualização do usuário deveria retornar True"
        usuario_db = prestador_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.nome == "Usuário Atualizado", "O nome do usuário atualizado não confere"
        assert usuario_db.telefone == "(28) 88888-0000", "O telefone do usuário atualizado não confere"
        assert usuario_db.email == "usuario_atualizado@email.com", "O email do usuário atualizado não confere"
        assert usuario_db.senha_hash == "123456", "A senha hash do usuário atualizado não confere"
        assert usuario_db.tipo == "ADMIN", "O tipo do usuário atualizado não confere"

    def test_atualizar_usuario_inexistente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        usuario_exemplo.id = 999  # ID que não existe
        # Act
        resultado = prestador_repo.atualizar_usuario(usuario_exemplo)
        # Assert
        assert resultado == False, "A atualização de um usuário inexistente deveria retornar False"

    def test_excluir_usuario_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()        
        id_usuario_inserido = prestador_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = prestador_repo.excluir_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        usuario_excluido = prestador_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_excluido is None, "O usuário excluído deveria ser None"

    def test_excluir_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        # Act
        resultado = prestador_repo.excluir_usuario(999)
        # Assert
        assert resultado == False, "A exclusão de um usuário inexistente deveria retornar False"

    def test_atualizar_senha_usuario(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        id_usuario_inserido = prestador_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = prestador_repo.atualizar_senha_usuario(id_usuario_inserido, "nova_senha_hash")
        # Assert
        assert resultado == True, "A atualização da senha do usuário deveria retornar True"
        usuario_db = prestador_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.senha_hash == "nova_senha_hash", "A senha do usuário atualizado não confere"

    def test_atualizar_senha_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        # Act
        resultado = prestador_repo.atualizar_senha_usuario(999, "nova_senha_hash")
        # Assert
        assert resultado == False, "A atualização da senha de um usuário inexistente deveria retornar False"

    def test_obter_usuarios_por_pagina_primeira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        for usuario in lista_usuarios_exemplo:
            prestador_repo.inserir_usuario(usuario)
        # Act
        pagina_usuarios = prestador_repo.obter_usuarios_por_pagina(1, 4)
        # Assert
        assert len(pagina_usuarios) == 4, "Deveria retornar 4 usuários na primeira página"
        assert all(isinstance(u, Usuario) for u in pagina_usuarios), "Todos os itens da página devem ser do tipo Usuario"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_usuarios]
        assert ids_esperados == ids_retornados, "Os IDs dos usuários na primeira página não estão corretos"
    
    def test_obter_usuarios_por_pagina_terceira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        prestador_repo.criar_tabela_prestadores()
        for usuario in lista_usuarios_exemplo:
            prestador_repo.inserir_usuario(usuario)
        # Act: busca a terceira página com 4 usuários por página
        pagina_usuarios = prestador_repo.obter_usuarios_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 usuários na terceira página)
        assert len(pagina_usuarios) == 2, "Deveria retornar 2 usuários na terceira página"
        assert (isinstance(u, Usuario) for u in pagina_usuarios), "Todos os itens da página devem ser do tipo Usuario"