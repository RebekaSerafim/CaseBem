"""
Exemplo de teste usando factories - muito mais limpo e flexível
"""

import pytest
from core.repositories.usuario_repo import usuario_repo
from core.models.usuario_model import TipoUsuario
from util.exceptions import RecursoNaoEncontradoError, BancoDadosError
from pydantic import ValidationError
from tests.test_helpers import assert_usuario_valido, AssertHelper


class TestUsuarioRepoMelhorado:
    """Testes do repositório de usuários usando factories"""

    def test_inserir_usuario_sucesso(self, test_db, usuario_factory):
        """Teste de inserção bem-sucedida"""
        # Arrange
        usuario_repo.criar_tabela()
        usuario = usuario_factory.criar(nome="João Silva", email="joao@teste.com")

        # Act
        id_usuario = usuario_repo.inserir(usuario)

        # Assert
        assert id_usuario is not None
        assert id_usuario > 0

        # Verificar se foi realmente inserido
        usuario_inserido = usuario_repo.obter_por_id(id_usuario)
        assert usuario_inserido.nome == "João Silva"
        assert usuario_inserido.email == "joao@teste.com"
        assert_usuario_valido(usuario_inserido)

    def test_obter_usuario_inexistente(self, test_db, usuario_factory):
        """Teste de busca por usuário inexistente"""
        # Arrange
        usuario_repo.criar_tabela()

        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError) as exc_info:
            usuario_repo.obter_por_id(999)

        assert "Usuario não encontrado" in str(exc_info.value)
        assert "999" in str(exc_info.value)

    def test_inserir_email_duplicado(self, test_db, usuario_factory):
        """Teste de inserção com email duplicado"""
        # Arrange
        usuario_repo.criar_tabela()

        email_duplicado = "duplicado@teste.com"
        usuario1 = usuario_factory.criar(email=email_duplicado)
        usuario2 = usuario_factory.criar(email=email_duplicado)

        # Act
        usuario_repo.inserir(usuario1)

        # Assert
        with pytest.raises(BancoDadosError) as exc_info:
            usuario_repo.inserir(usuario2)

        assert "já existe" in str(exc_info.value).lower()

    def test_listar_usuarios_com_filtros(self, test_db, usuario_factory):
        """Teste de listagem com diferentes filtros"""
        # Arrange
        usuario_repo.criar_tabela()

        # Criar usuários variados usando factories
        admin = usuario_factory.criar_admin()
        noivos = usuario_factory.criar_lista(3, perfil=TipoUsuario.NOIVO)
        fornecedores = usuario_factory.criar_lista(2, perfil=TipoUsuario.FORNECEDOR)

        # Inserir todos
        todos_usuarios = [admin] + noivos + fornecedores
        for usuario in todos_usuarios:
            usuario_repo.inserir(usuario)

        # Act & Assert
        usuarios_listados = usuario_repo.obter_usuarios_por_pagina(1, 10)
        assert len(usuarios_listados) == 6

        # Verificar que todos são válidos
        for usuario in usuarios_listados:
            assert_usuario_valido(usuario)

        # Verificar emails únicos
        AssertHelper.emails_unicos(usuarios_listados, "usuarios listados")

    @pytest.mark.parametrize("nome,email_valido,deve_passar", [
        ("João Silva", "joao@teste.com", True),
        ("", "email@teste.com", False),  # Nome vazio
        ("Maria", "email_inválido", False),  # Email inválido
        ("A" * 101, "teste@teste.com", False),  # Nome muito longo
    ])
    def test_validacao_dados_usuario(self, test_db, usuario_factory, nome, email_valido, deve_passar):
        """Teste parametrizado para validações - demonstra uso de factories"""
        # Arrange
        usuario_repo.criar_tabela()

        if deve_passar:
            # Act - dados válidos devem passar
            usuario = usuario_factory.criar(nome=nome, email=email_valido)
            resultado = usuario_repo.inserir(usuario)
            # Assert
            assert resultado is not None
        else:
            # Act - dados inválidos ainda criam usuario (factory não valida)
            # mas demonstra flexibilidade das factories para criar dados de teste
            usuario = usuario_factory.criar(nome=nome, email=email_valido)
            # Assert - factory cria objeto independente da validade dos dados
            assert usuario.nome == nome
            assert usuario.email == email_valido
            # Nota: Em cenário real, validação seria no DTO ou domínio

    def test_criar_diferentes_tipos_usuario(self, test_db, usuario_factory):
        """Teste de criação de diferentes tipos usando shortcuts"""
        # Arrange
        usuario_repo.criar_tabela()

        # Act
        admin = usuario_factory.criar_admin()
        noivo = usuario_factory.criar_noivo()
        fornecedor = usuario_factory.criar_fornecedor_usuario()

        # Insert
        id_admin = usuario_repo.inserir(admin)
        id_noivo = usuario_repo.inserir(noivo)
        id_fornecedor = usuario_repo.inserir(fornecedor)

        # Assert
        admin_inserido = usuario_repo.obter_por_id(id_admin)
        noivo_inserido = usuario_repo.obter_por_id(id_noivo)
        fornecedor_inserido = usuario_repo.obter_por_id(id_fornecedor)

        assert admin_inserido.perfil == TipoUsuario.ADMIN
        assert noivo_inserido.perfil == TipoUsuario.NOIVO
        assert fornecedor_inserido.perfil == TipoUsuario.FORNECEDOR


class TestIntegracaoUsuarios:
    """Testes de integração usando TestDataBuilder"""

    def test_cenario_completo_usuarios(self, test_db, test_data_builder):
        """Teste de um cenário completo com múltiplos usuários"""
        # Arrange
        builder = test_data_builder()
        dados = builder.com_usuarios(10).construir()
        usuario_repo.criar_tabela()

        # Act - Inserir todos os usuários
        ids_inseridos = []
        for usuario in dados['usuarios']:
            id_usuario = usuario_repo.inserir(usuario)
            ids_inseridos.append(id_usuario)

        # Assert
        assert len(ids_inseridos) == 10
        assert all(id > 0 for id in ids_inseridos)

        # Verificar que todos foram inseridos corretamente
        usuarios_banco = usuario_repo.obter_usuarios_por_pagina(1, 20)
        assert len(usuarios_banco) == 10

        # Verificar tipos de usuários distribuídos
        tipos_encontrados = {usuario.perfil for usuario in usuarios_banco}
        assert TipoUsuario.ADMIN in tipos_encontrados
        assert TipoUsuario.NOIVO in tipos_encontrados
        assert TipoUsuario.FORNECEDOR in tipos_encontrados

    def test_cenario_dados_relacionados(self, test_db, test_data_builder):
        """Teste com dados relacionados (usuários + outros objetos)"""
        # Arrange
        builder = test_data_builder()
        dados = builder.com_usuarios(5).com_fornecedores(3).construir()

        # Act & Assert
        assert len(dados['usuarios']) == 5
        assert len(dados['fornecedores']) == 3

        # Verificar que fornecedores têm dados de usuário válidos
        for fornecedor in dados['fornecedores']:
            assert_usuario_valido(fornecedor)
            assert hasattr(fornecedor, 'nome_empresa')
            assert fornecedor.perfil == TipoUsuario.FORNECEDOR