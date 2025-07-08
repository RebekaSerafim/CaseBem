from model.usuario_model import Usuario
from model.administrador_model import Administrador
from repo import administrador_repo, usuario_repo

class TestAdministradorRepo:
    def test_criar_tabela_administradores(self, test_db):
        # Arrange
        # Act
        resultado = administrador_repo.criar_tabela_administradores()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"        

    def test_inserir_administrador(self, test_db, administrador_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        # Act
        id_administrador_inserido = administrador_repo.inserir_administrador(administrador_exemplo)
        # Assert
        administrador_db = administrador_repo.obter_administrador_por_id(id_administrador_inserido)
        assert administrador_db is not None, "O administrador inserido não deveria ser None"
        assert administrador_db.id == 1, "O administrador inserido deveria ter um ID igual a 1"
        assert administrador_db.nome == "Administrador Teste", "O nome do administrador inserido não confere"
        assert administrador_db.telefone == "(28) 99999-9999", "O telefone do administrador inserido não confere"
        assert administrador_db.email == "administrador@email.com", "O email do administrador inserido não confere"
        assert administrador_db.senha_hash == "654321", "A senha hash do administrador inserido não confere"
        assert administrador_db.tipo == "ADMIN", "O tipo do administrador inserido não confere"

    def test_obter_administrador_por_id_existente(self, test_db, administrador_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        id_administrador_inserido = administrador_repo.inserir_administrador(administrador_exemplo)
        # Act
        administrador_db = administrador_repo.obter_administrador_por_id(id_administrador_inserido)
        # Assert
        assert administrador_db is not None, "O administrador retornado deveria ser diferente de None"
        assert administrador_db.id == id_administrador_inserido, "O id do administrador buscado deveria ser igual ao id do administrador inserido"
        assert administrador_db.nome == administrador_exemplo.nome, "O nome do administrador buscado deveria ser igual ao nome do administrador inserido"
        assert administrador_db.telefone == administrador_exemplo.telefone, "O telefone do administrador buscado deveria ser igual ao telefone do administrador inserido"
        assert administrador_db.email == administrador_exemplo.email, "O email do administrador buscado deveria ser igual ao email do administrador inserido"
        assert administrador_db.senha_hash == administrador_exemplo.senha_hash, "A senha hash do administrador buscado deveria ser igual à senha hash do administrador inserido"
        assert administrador_db.tipo == administrador_exemplo.tipo, "O tipo do administrador buscado deveria ser igual ao tipo do administrador inserido"

    def test_obter_administrador_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        # Act
        administrador_db = administrador_repo.obter_administrador_por_id(999)
        # Assert
        assert administrador_db is None, "O administrador buscado com ID inexistente deveria retornar None"

    def test_obter_usuario_por_email_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        id_usuario_inserido = administrador_repo.inserir_usuario(usuario_exemplo)
        # Act
        usuario_db = administrador_repo.obter_usuario_por_email(usuario_exemplo.email)
        # Assert
        assert usuario_db is not None, "O usuário buscado por email deveria ser diferente de None"
        assert usuario_db.id == id_usuario_inserido, "O id do usuário buscado por email deveria ser igual ao id do usuário inserido"
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário buscado deveria ser igual ao email do usuário inserido"

    def test_obter_usuario_por_email_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        # Act
        usuario_db = administrador_repo.obter_usuario_por_email("inexistente@email.com")
        # Assert
        assert usuario_db is None, "O usuário buscado por email inexistente deveria retornar None"

    def test_atualizar_usuario_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        id_usuario_inserido = administrador_repo.inserir_usuario(usuario_exemplo)
        usuario_inserido = administrador_repo.obter_usuario_por_id(id_usuario_inserido)
        # Act
        usuario_inserido.nome = "Usuário Atualizado"
        usuario_inserido.telefone = "(28) 88888-0000"
        usuario_inserido.email = "usuario_atualizado@email.com"
        resultado = administrador_repo.atualizar_usuario(usuario_inserido)
        # Assert
        assert resultado == True, "A atualização do usuário deveria retornar True"
        usuario_db = administrador_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.nome == "Usuário Atualizado", "O nome do usuário atualizado não confere"
        assert usuario_db.telefone == "(28) 88888-0000", "O telefone do usuário atualizado não confere"
        assert usuario_db.email == "usuario_atualizado@email.com", "O email do usuário atualizado não confere"
        assert usuario_db.senha_hash == "123456", "A senha hash do usuário atualizado não confere"
        assert usuario_db.tipo == "ADMIN", "O tipo do usuário atualizado não confere"

    def test_atualizar_usuario_inexistente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        usuario_exemplo.id = 999  # ID que não existe
        # Act
        resultado = administrador_repo.atualizar_usuario(usuario_exemplo)
        # Assert
        assert resultado == False, "A atualização de um usuário inexistente deveria retornar False"

    def test_excluir_usuario_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()        
        id_usuario_inserido = administrador_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = administrador_repo.excluir_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "O resultado da exclusão deveria ser True"
        usuario_excluido = administrador_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_excluido is None, "O usuário excluído deveria ser None"

    def test_excluir_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        # Act
        resultado = administrador_repo.excluir_usuario(999)
        # Assert
        assert resultado == False, "A exclusão de um usuário inexistente deveria retornar False"

    def test_atualizar_senha_usuario(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        id_usuario_inserido = administrador_repo.inserir_usuario(usuario_exemplo)
        # Act
        resultado = administrador_repo.atualizar_senha_usuario(id_usuario_inserido, "nova_senha_hash")
        # Assert
        assert resultado == True, "A atualização da senha do usuário deveria retornar True"
        usuario_db = administrador_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.senha_hash == "nova_senha_hash", "A senha do usuário atualizado não confere"

    def test_atualizar_senha_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        # Act
        resultado = administrador_repo.atualizar_senha_usuario(999, "nova_senha_hash")
        # Assert
        assert resultado == False, "A atualização da senha de um usuário inexistente deveria retornar False"

    def test_obter_usuarios_por_pagina_primeira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        for usuario in lista_usuarios_exemplo:
            administrador_repo.inserir_usuario(usuario)
        # Act
        pagina_usuarios = administrador_repo.obter_usuarios_por_pagina(1, 4)
        # Assert
        assert len(pagina_usuarios) == 4, "Deveria retornar 4 usuários na primeira página"
        assert all(isinstance(u, Usuario) for u in pagina_usuarios), "Todos os itens da página devem ser do tipo Usuario"
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [u.id for u in pagina_usuarios]
        assert ids_esperados == ids_retornados, "Os IDs dos usuários na primeira página não estão corretos"
    
    def test_obter_usuarios_por_pagina_terceira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        administrador_repo.criar_tabela_administradores()
        for usuario in lista_usuarios_exemplo:
            administrador_repo.inserir_usuario(usuario)
        # Act: busca a terceira página com 4 usuários por página
        pagina_usuarios = administrador_repo.obter_usuarios_por_pagina(3, 4)
        # Assert: verifica se retornou a quantidade correta (2 usuários na terceira página)
        assert len(pagina_usuarios) == 2, "Deveria retornar 2 usuários na terceira página"
        assert (isinstance(u, Usuario) for u in pagina_usuarios), "Todos os itens da página devem ser do tipo Usuario"