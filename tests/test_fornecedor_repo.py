import pytest
from core.models.fornecedor_model import Fornecedor
from core.models.usuario_model import TipoUsuario
from core.repositories.fornecedor_repo import fornecedor_repo
from core.repositories.usuario_repo import usuario_repo
from util.exceptions import RecursoNaoEncontradoError

class TestFornecedorRepo:
    def test_criar_tabela_fornecedor(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        # Act
        resultado = fornecedor_repo.criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        # Assert
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor_inserido)
        assert fornecedor_db is not None, "O fornecedor inserido não deveria ser None"
        assert fornecedor_db.id == id_fornecedor_inserido, "O ID do fornecedor inserido deveria ser igual ao retornado"
        assert fornecedor_db.nome == fornecedor_exemplo.nome, "O nome do fornecedor inserido não confere"
        assert fornecedor_db.cpf == fornecedor_exemplo.cpf, "O CPF do fornecedor inserido não confere"
        assert fornecedor_db.email == fornecedor_exemplo.email, "O email do fornecedor inserido não confere"
        assert fornecedor_db.perfil.value == "FORNECEDOR", "O perfil do fornecedor inserido não confere"
        assert fornecedor_db.nome_empresa == fornecedor_exemplo.nome_empresa, "O nome da empresa não confere"

    def test_obter_fornecedor_por_id_existente(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        # Act
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor_inserido)
        # Assert
        assert fornecedor_db is not None, "O fornecedor retornado deveria ser diferente de None"
        assert fornecedor_db.id == id_fornecedor_inserido, "O ID do fornecedor retornado deveria ser igual ao inserido"

    def test_obter_fornecedor_por_id_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            fornecedor_repo.obter_por_id(999)

    def test_atualizar_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        fornecedor_exemplo.id = id_fornecedor_inserido
        fornecedor_exemplo.nome_empresa = "Empresa Atualizada"
        fornecedor_exemplo.descricao = "Nova descrição"
        # Act
        resultado = fornecedor_repo.atualizar(fornecedor_exemplo)
        # Assert
        assert resultado == True, "A atualização deveria retornar True"
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor_inserido)
        assert fornecedor_db.nome_empresa == "Empresa Atualizada", "O nome da empresa deveria ter sido atualizado"
        assert fornecedor_db.descricao == "Nova descrição", "A descrição deveria ter sido atualizada"

    def test_excluir_fornecedor(self, test_db, fornecedor_exemplo):
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        id_fornecedor_inserido = fornecedor_repo.inserir(fornecedor_exemplo)
        # Act
        assert id_fornecedor_inserido is not None
        resultado = fornecedor_repo.excluir(id_fornecedor_inserido)
        # Assert
        assert resultado == True, "A exclusão deveria retornar True"
        with pytest.raises(RecursoNaoEncontradoError):
            fornecedor_repo.obter_por_id(id_fornecedor_inserido)

    def test_excluir_fornecedor_inexistente(self, test_db):
        """Testa exclusão de fornecedor inexistente (linha 130)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act
        resultado = fornecedor_repo.excluir(999)
        # Assert
        assert resultado == False, "Deveria retornar False ao excluir fornecedor inexistente"

    def test_atualizar_fornecedor_inexistente(self, test_db, fornecedor_exemplo):
        """Testa atualização de fornecedor inexistente (linhas 107-109)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        fornecedor_exemplo.id = 999
        # Act
        resultado = fornecedor_repo.atualizar(fornecedor_exemplo)
        # Assert
        assert resultado == False, "Deveria retornar False ao atualizar fornecedor inexistente"

    def test_contar_nao_verificados(self, test_db, fornecedor_factory):
        """Testa contagem de fornecedores não verificados (linhas 136-141)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Criar fornecedores com diferentes status de verificação
        fornecedor1 = fornecedor_factory.criar(verificado=False)
        fornecedor2 = fornecedor_factory.criar(verificado=False)
        fornecedor3 = fornecedor_factory.criar(verificado=True)
        fornecedor_repo.inserir(fornecedor1)
        fornecedor_repo.inserir(fornecedor2)
        fornecedor_repo.inserir(fornecedor3)
        # Act
        total_nao_verificados = fornecedor_repo.contar_nao_verificados()
        # Assert
        assert total_nao_verificados == 2, "Deveria ter 2 fornecedores não verificados"

    def test_rejeitar_fornecedor(self, test_db, fornecedor_factory):
        """Testa rejeição de fornecedor (linhas 145-154)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        fornecedor = fornecedor_factory.criar(verificado=True)
        id_fornecedor = fornecedor_repo.inserir(fornecedor)
        assert id_fornecedor is not None
        # Act
        resultado = fornecedor_repo.rejeitar(id_fornecedor)
        # Assert
        assert resultado == True, "Rejeição deveria retornar True"
        fornecedor_db = fornecedor_repo.obter_por_id(id_fornecedor)
        assert fornecedor_db.verificado == False, "Fornecedor deveria estar não verificado"

    def test_rejeitar_fornecedor_inexistente(self, test_db):
        """Testa rejeição de fornecedor inexistente (linha 151-153)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act
        resultado = fornecedor_repo.rejeitar(999)
        # Assert
        assert resultado == False, "Deveria retornar False ao rejeitar fornecedor inexistente"

    def test_obter_fornecedor_por_cnpj(self, test_db, fornecedor_factory):
        """Testa obtenção de fornecedor por CNPJ (linhas 158-170)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        fornecedor = fornecedor_factory.criar(cnpj="12345678901234")
        fornecedor_repo.inserir(fornecedor)
        # Act
        fornecedor_db = fornecedor_repo.obter_fornecedor_por_cnpj("12345678901234")
        # Assert
        assert fornecedor_db is not None, "Fornecedor deveria ser encontrado"
        assert fornecedor_db.cnpj == "12345678901234"

    def test_obter_fornecedor_por_cnpj_inexistente(self, test_db):
        """Testa exceção ao buscar CNPJ inexistente (linha 170)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError) as exc_info:
            fornecedor_repo.obter_fornecedor_por_cnpj("99999999999999")
        assert "Fornecedor" in str(exc_info.value)

    def test_obter_fornecedores_por_pagina(self, test_db, fornecedor_factory):
        """Testa obtenção paginada de fornecedores (linhas 174-178)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        for i in range(5):
            fornecedor = fornecedor_factory.criar()
            fornecedor_repo.inserir(fornecedor)
        # Act
        fornecedores_pag1 = fornecedor_repo.obter_fornecedores_por_pagina(pagina=1, tamanho_pagina=2)
        fornecedores_pag2 = fornecedor_repo.obter_fornecedores_por_pagina(pagina=2, tamanho_pagina=2)
        # Assert
        assert len(fornecedores_pag1) == 2, "Primeira página deveria ter 2 fornecedores"
        assert len(fornecedores_pag2) == 2, "Segunda página deveria ter 2 fornecedores"

    def test_obter_fornecedores_verificados(self, test_db, fornecedor_factory):
        """Testa obtenção de fornecedores verificados (linhas 182-193)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        fornecedor1 = fornecedor_factory.criar(verificado=True)
        fornecedor2 = fornecedor_factory.criar(verificado=False)
        fornecedor3 = fornecedor_factory.criar(verificado=True)
        fornecedor_repo.inserir(fornecedor1)
        fornecedor_repo.inserir(fornecedor2)
        fornecedor_repo.inserir(fornecedor3)
        # Act
        fornecedores_verificados = fornecedor_repo.obter_fornecedores_verificados()
        # Assert
        assert len(fornecedores_verificados) == 2, "Deveria ter 2 fornecedores verificados"
        assert all(f.verificado for f in fornecedores_verificados), "Todos deveriam estar verificados"

    def test_buscar_fornecedores(self, test_db, fornecedor_factory):
        """Testa busca de fornecedores por nome (linhas 197-209)"""
        # Arrange
        usuario_repo.criar_tabela()
        fornecedor_repo.criar_tabela()
        fornecedor1 = fornecedor_factory.criar(nome="João Silva", nome_empresa="Empresa A")
        fornecedor2 = fornecedor_factory.criar(nome="Maria Santos", nome_empresa="Empresa João")
        fornecedor3 = fornecedor_factory.criar(nome="Pedro Costa", nome_empresa="Empresa B")
        fornecedor_repo.inserir(fornecedor1)
        fornecedor_repo.inserir(fornecedor2)
        fornecedor_repo.inserir(fornecedor3)
        # Act
        resultados = fornecedor_repo.buscar_fornecedores("João")
        # Assert
        assert len(resultados) == 2, "Deveria encontrar 2 fornecedores com 'João'"
        nomes = [f.nome for f in resultados if f.nome] + [f.nome_empresa for f in resultados if f.nome_empresa]
        assert any("João" in nome for nome in nomes)

