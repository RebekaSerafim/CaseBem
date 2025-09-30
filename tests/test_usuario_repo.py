"""
Testes do repositório de usuários usando o novo sistema de factories
Demonstra as melhores práticas com Factory Pattern e test helpers
"""

from core.models.usuario_model import Usuario, TipoUsuario
from core.repositories import usuario_repo
from util.exceptions import RecursoNaoEncontradoError, BancoDadosError
from tests.test_helpers import assert_usuario_valido, AssertHelper
import pytest


class TestUsuarioRepo:
    """Testes do repositório de usuários com factories"""

    def test_criar_tabela_usuarios(self, test_db):
        """Teste de criação de tabela"""
        resultado = usuario_repo.criar_tabela_usuarios()
        assert resultado == True

    def test_inserir_usuario_com_factory(self, test_db, usuario_factory):
        """Teste de inserção usando factory"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuario = usuario_factory.criar(nome="João Silva", email="joao@teste.com")

        # Act
        id_usuario_inserido = usuario_repo.inserir_usuario(usuario)

        # Assert
        usuario_db = usuario_repo.obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None
        assert usuario_db.id == 1
        assert usuario_db.nome == "João Silva"
        assert usuario_db.email == "joao@teste.com"
        assert_usuario_valido(usuario_db)

    def test_inserir_diferentes_tipos_usuario(self, test_db, usuario_factory):
        """Demonstra uso dos shortcuts das factories"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()

        # Act - Usar shortcuts da factory
        admin = usuario_factory.criar_admin()
        noivo = usuario_factory.criar_noivo()
        fornecedor = usuario_factory.criar_fornecedor_usuario()

        id_admin = usuario_repo.inserir_usuario(admin)
        id_noivo = usuario_repo.inserir_usuario(noivo)
        id_fornecedor = usuario_repo.inserir_usuario(fornecedor)

        # Assert
        admin_db = usuario_repo.obter_usuario_por_id(id_admin)
        noivo_db = usuario_repo.obter_usuario_por_id(id_noivo)
        fornecedor_db = usuario_repo.obter_usuario_por_id(id_fornecedor)

        assert admin_db.perfil == TipoUsuario.ADMIN
        assert noivo_db.perfil == TipoUsuario.NOIVO
        assert fornecedor_db.perfil == TipoUsuario.FORNECEDOR

        # Usar helpers para validar
        for usuario in [admin_db, noivo_db, fornecedor_db]:
            assert_usuario_valido(usuario)

    def test_inserir_lista_usuarios_variados(self, test_db, usuario_factory):
        """Demonstra criação de lista com factory"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuarios = usuario_factory.criar_lista(5)  # 5 usuários variados

        # Act
        ids_inseridos = []
        for usuario in usuarios:
            id_inserido = usuario_repo.inserir_usuario(usuario)
            ids_inseridos.append(id_inserido)

        # Assert
        assert len(ids_inseridos) == 5
        usuarios_db = usuario_repo.obter_usuarios_por_pagina(1, 10)
        assert len(usuarios_db) == 5

        # Usar AssertHelper para validações complexas
        AssertHelper.emails_unicos(usuarios_db, "usuários da lista")
        for usuario in usuarios_db:
            assert_usuario_valido(usuario)

    def test_obter_usuario_por_id_inexistente(self, test_db):
        """Teste com novo sistema de exceptions"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()

        # Act & Assert - usar nova exception
        with pytest.raises(RecursoNaoEncontradoError) as exc_info:
            usuario_repo.obter_usuario_por_id(999)

        assert "Usuario não encontrado" in str(exc_info.value)
        assert "999" in str(exc_info.value)

    def test_email_duplicado_com_factory(self, test_db, usuario_factory):
        """Teste de constraint de email único"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        email_duplicado = "duplicado@teste.com"

        usuario1 = usuario_factory.criar(email=email_duplicado)
        usuario2 = usuario_factory.criar(email=email_duplicado)

        # Act
        usuario_repo.inserir_usuario(usuario1)

        # Assert - nova exception
        with pytest.raises(BancoDadosError) as exc_info:
            usuario_repo.inserir_usuario(usuario2)

        assert "já existe" in str(exc_info.value).lower()

    def test_atualizar_usuario_com_factory(self, test_db, usuario_factory):
        """Teste de atualização usando factory"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuario = usuario_factory.criar(nome="Nome Original")
        id_inserido = usuario_repo.inserir_usuario(usuario)

        # Act
        usuario_para_atualizar = usuario_repo.obter_usuario_por_id(id_inserido)
        usuario_para_atualizar.nome = "Nome Atualizado"
        resultado = usuario_repo.atualizar_usuario(usuario_para_atualizar)

        # Assert
        assert resultado == True
        usuario_atualizado = usuario_repo.obter_usuario_por_id(id_inserido)
        assert usuario_atualizado.nome == "Nome Atualizado"
        assert_usuario_valido(usuario_atualizado)

    def test_paginacao_com_factory(self, test_db, usuario_factory):
        """Teste de paginação usando factory"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        usuarios = usuario_factory.criar_lista(10)

        for usuario in usuarios:
            usuario_repo.inserir_usuario(usuario)

        # Act
        primeira_pagina = usuario_repo.obter_usuarios_por_pagina(1, 4)
        segunda_pagina = usuario_repo.obter_usuarios_por_pagina(2, 4)
        terceira_pagina = usuario_repo.obter_usuarios_por_pagina(3, 4)

        # Assert
        assert len(primeira_pagina) == 4
        assert len(segunda_pagina) == 4
        assert len(terceira_pagina) == 2  # Últimos 2

        # Verificar que todos são válidos
        todas_paginas = primeira_pagina + segunda_pagina + terceira_pagina
        for usuario in todas_paginas:
            assert_usuario_valido(usuario)

        # Verificar IDs únicos em todas as páginas
        AssertHelper.ids_unicos(todas_paginas, "todas as páginas")

    def test_cenario_integrado_com_data_builder(self, test_db, test_data_builder):
        """Teste de integração usando TestDataBuilder"""
        # Arrange
        usuario_repo.criar_tabela_usuarios()
        builder = test_data_builder()
        dados = builder.com_usuarios(8).construir()

        # Act - Inserir usuários do builder
        ids_inseridos = []
        for usuario in dados['usuarios']:
            id_inserido = usuario_repo.inserir_usuario(usuario)
            ids_inseridos.append(id_inserido)

        # Assert
        assert len(ids_inseridos) == 8
        todos_usuarios = usuario_repo.obter_usuarios_por_pagina(1, 20)
        assert len(todos_usuarios) == 8

        # Verificar distribuição de tipos
        tipos_encontrados = {usuario.perfil for usuario in todos_usuarios}
        assert TipoUsuario.ADMIN in tipos_encontrados
        assert TipoUsuario.NOIVO in tipos_encontrados
        assert TipoUsuario.FORNECEDOR in tipos_encontrados

        AssertHelper.emails_unicos(todos_usuarios, "todos os usuários")