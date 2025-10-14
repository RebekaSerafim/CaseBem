"""
Testes para BaseRepo e BaseRepoChaveComposta
"""
import pytest
from dataclasses import dataclass
from typing import List, Dict, Any
from core.repositories.base_repo import BaseRepo, BaseRepoChaveComposta
from util.exceptions import RecursoNaoEncontradoError, BancoDadosError, ValidacaoError


# Mock SQL module para BaseRepo
class MockSQL:
    CRIAR_TABELA = """
        CREATE TABLE IF NOT EXISTS mock_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ativo INTEGER DEFAULT 1
        )
    """
    INSERIR = "INSERT INTO mock_table (nome, ativo) VALUES (?, ?)"
    ATUALIZAR = "UPDATE mock_table SET nome = ?, ativo = ? WHERE id = ?"
    EXCLUIR = "DELETE FROM mock_table WHERE id = ?"
    OBTER_POR_ID = "SELECT * FROM mock_table WHERE id = ?"
    LISTAR_TODOS = "SELECT * FROM mock_table"
    LISTAR_ATIVOS = "SELECT * FROM mock_table WHERE ativo = 1"
    LISTAR_INATIVOS = "SELECT * FROM mock_table WHERE ativo = 0"


# Mock SQL module para BaseRepoChaveComposta
class MockCompostaSQL:
    CRIAR_TABELA = """
        CREATE TABLE IF NOT EXISTS mock_composta (
            id_a INTEGER NOT NULL,
            id_b INTEGER NOT NULL,
            valor TEXT,
            PRIMARY KEY (id_a, id_b)
        )
    """
    INSERIR = "INSERT INTO mock_composta (id_a, id_b, valor) VALUES (?, ?, ?)"
    ATUALIZAR = "UPDATE mock_composta SET valor = ? WHERE id_a = ? AND id_b = ?"
    EXCLUIR = "DELETE FROM mock_composta WHERE id_a = ? AND id_b = ?"
    OBTER_POR_CHAVE = "SELECT * FROM mock_composta WHERE id_a = ? AND id_b = ?"
    LISTAR_TODOS = "SELECT * FROM mock_composta"


@dataclass
class MockModel:
    """Modelo mock para testes"""
    id: int
    nome: str
    ativo: bool = True


@dataclass
class MockCompostaModel:
    """Modelo mock com chave composta para testes"""
    id_a: int
    id_b: int
    valor: str


class MockRepo(BaseRepo):
    """Repositório mock para testar BaseRepo"""

    def __init__(self):
        super().__init__("mock_table", MockModel, MockSQL)

    def _objeto_para_tupla_insert(self, objeto: MockModel) -> tuple:
        return (objeto.nome, objeto.ativo)

    def _objeto_para_tupla_update(self, objeto: MockModel) -> tuple:
        return (objeto.nome, objeto.ativo, objeto.id)

    def _linha_para_objeto(self, linha: Dict) -> MockModel:
        return MockModel(
            id=self._safe_get(linha, "id"),
            nome=self._safe_get(linha, "nome", ""),
            ativo=bool(self._safe_get(linha, "ativo", True)),
        )


class MockCompostaRepo(BaseRepoChaveComposta):
    """Repositório mock para testar BaseRepoChaveComposta"""

    def __init__(self):
        super().__init__(
            "mock_composta", MockCompostaModel, MockCompostaSQL, ["id_a", "id_b"]
        )

    def _objeto_para_tupla_insert(self, objeto: MockCompostaModel) -> tuple:
        return (objeto.id_a, objeto.id_b, objeto.valor)

    def _objeto_para_tupla_update(self, objeto: MockCompostaModel) -> tuple:
        return (objeto.valor, objeto.id_a, objeto.id_b)

    def _linha_para_objeto(self, linha: Dict) -> MockCompostaModel:
        return MockCompostaModel(
            id_a=self._safe_get(linha, "id_a"),
            id_b=self._safe_get(linha, "id_b"),
            valor=self._safe_get(linha, "valor", ""),
        )


class TestBaseRepo:
    """Testes para BaseRepo"""

    def test_criar_tabela(self, test_db):
        """Testa criação de tabela"""
        # Arrange
        repo = MockRepo()
        # Act
        resultado = repo.criar_tabela()
        # Assert
        assert resultado is True

    def test_inserir(self, test_db):
        """Testa inserção de registro"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        obj = MockModel(id=0, nome="Teste")
        # Act
        id_inserido = repo.inserir(obj)
        # Assert
        assert id_inserido > 0
        obj_db = repo.obter_por_id(id_inserido)
        assert obj_db.nome == "Teste"

    def test_atualizar_nao_existe(self, test_db):
        """Testa atualização de registro que não existe (linha 89)"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        obj = MockModel(id=999, nome="Não existe")
        # Act
        resultado = repo.atualizar(obj)
        # Assert
        assert resultado is False

    def test_atualizar(self, test_db):
        """Testa atualização de registro"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        obj = MockModel(id=0, nome="Original")
        id_inserido = repo.inserir(obj)
        obj.id = id_inserido
        obj.nome = "Atualizado"
        # Act
        resultado = repo.atualizar(obj)
        # Assert
        assert resultado is True
        obj_db = repo.obter_por_id(id_inserido)
        assert obj_db.nome == "Atualizado"

    def test_excluir(self, test_db):
        """Testa exclusão de registro"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        obj = MockModel(id=0, nome="Para excluir")
        id_inserido = repo.inserir(obj)
        # Act
        resultado = repo.excluir(id_inserido)
        # Assert
        assert resultado is True
        with pytest.raises(RecursoNaoEncontradoError):
            repo.obter_por_id(id_inserido)

    def test_excluir_nao_existe(self, test_db):
        """Testa exclusão de registro que não existe (linha 111)"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        # Act
        resultado = repo.excluir(999)
        # Assert
        assert resultado is False

    def test_excluir_id_invalido(self, test_db):
        """Testa exclusão com ID inválido (linha 101)"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(ValidacaoError) as exc_info:
            repo.excluir(0)
        assert "ID deve ser um número positivo" in str(exc_info.value)

    def test_excluir_id_negativo(self, test_db):
        """Testa exclusão com ID negativo"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(ValidacaoError) as exc_info:
            repo.excluir(-1)
        assert "ID deve ser um número positivo" in str(exc_info.value)

    def test_obter_por_id(self, test_db):
        """Testa obtenção por ID"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        obj = MockModel(id=0, nome="Buscar")
        id_inserido = repo.inserir(obj)
        # Act
        obj_db = repo.obter_por_id(id_inserido)
        # Assert
        assert obj_db.nome == "Buscar"

    def test_obter_por_id_invalido(self, test_db):
        """Testa obtenção com ID inválido (linha 122)"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(ValidacaoError) as exc_info:
            repo.obter_por_id(0)
        assert "ID deve ser um número positivo" in str(exc_info.value)

    def test_obter_por_id_negativo(self, test_db):
        """Testa obtenção com ID negativo"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(ValidacaoError) as exc_info:
            repo.obter_por_id(-5)
        assert "ID deve ser um número positivo" in str(exc_info.value)

    def test_obter_por_id_nao_existe(self, test_db):
        """Testa obtenção de ID que não existe"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            repo.obter_por_id(999)

    def test_listar_todos(self, test_db):
        """Testa listagem de todos os registros"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        repo.inserir(MockModel(id=0, nome="Item 1"))
        repo.inserir(MockModel(id=0, nome="Item 2"))
        # Act
        lista = repo.listar_todos()
        # Assert
        assert len(lista) == 2

    def test_listar_todos_ativos(self, test_db):
        """Testa listagem de registros ativos"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        id1 = repo.inserir(MockModel(id=0, nome="Ativo", ativo=True))
        id2 = repo.inserir(MockModel(id=0, nome="Inativo", ativo=False))
        # Act
        lista = repo.listar_todos(ativo=True)
        # Assert
        assert len(lista) == 1
        assert lista[0].nome == "Ativo"

    def test_listar_todos_inativos(self, test_db):
        """Testa listagem de registros inativos"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        id1 = repo.inserir(MockModel(id=0, nome="Ativo", ativo=True))
        id2 = repo.inserir(MockModel(id=0, nome="Inativo", ativo=False))
        # Act
        lista = repo.listar_todos(ativo=False)
        # Assert
        assert len(lista) == 1
        assert lista[0].nome == "Inativo"

    def test_executar_consulta(self, test_db):
        """Testa execução de consulta customizada"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        repo.inserir(MockModel(id=0, nome="Teste SQL"))
        # Act
        resultados = repo.executar_consulta(
            "SELECT * FROM mock_table WHERE nome = ?", ("Teste SQL",)
        )
        # Assert
        assert len(resultados) == 1
        assert resultados[0]["nome"] == "Teste SQL"

    def test_executar_comando(self, test_db):
        """Testa execução de comando SQL"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        id_inserido = repo.inserir(MockModel(id=0, nome="Original"))
        # Act
        resultado = repo.executar_comando(
            "UPDATE mock_table SET nome = ? WHERE id = ?", ("Modificado", id_inserido)
        )
        # Assert
        assert resultado is True
        obj_db = repo.obter_por_id(id_inserido)
        assert obj_db.nome == "Modificado"

    def test_contar_registros(self, test_db):
        """Testa contagem de registros"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        repo.inserir(MockModel(id=0, nome="Item 1"))
        repo.inserir(MockModel(id=0, nome="Item 2"))
        repo.inserir(MockModel(id=0, nome="Item 3"))
        # Act
        total = repo.contar_registros()
        # Assert
        assert total == 3

    def test_contar_registros_com_condicao(self, test_db):
        """Testa contagem de registros com condição WHERE"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        repo.inserir(MockModel(id=0, nome="Ativo", ativo=True))
        repo.inserir(MockModel(id=0, nome="Inativo", ativo=False))
        # Act
        total = repo.contar_registros("ativo = ?", (1,))
        # Assert
        assert total == 1

    def test_contar(self, test_db):
        """Testa método contar() alias (linha 242)"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        repo.inserir(MockModel(id=0, nome="Item 1"))
        repo.inserir(MockModel(id=0, nome="Item 2"))
        # Act
        total = repo.contar()
        # Assert
        assert total == 2

    def test_obter_paginado(self, test_db):
        """Testa obtenção paginada de registros"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        for i in range(5):
            repo.inserir(MockModel(id=0, nome=f"Item {i+1}"))
        # Act
        objetos, total = repo.obter_paginado(pagina=1, tamanho_pagina=2)
        # Assert
        assert len(objetos) == 2
        assert total == 5

    def test_ativar(self, test_db):
        """Testa ativação de registro"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        id_inserido = repo.inserir(MockModel(id=0, nome="Item", ativo=False))
        # Act
        resultado = repo.ativar(id_inserido)
        # Assert
        assert resultado is True
        obj_db = repo.obter_por_id(id_inserido)
        assert obj_db.ativo is True

    def test_desativar(self, test_db):
        """Testa desativação de registro"""
        # Arrange
        repo = MockRepo()
        repo.criar_tabela()
        id_inserido = repo.inserir(MockModel(id=0, nome="Item", ativo=True))
        # Act
        resultado = repo.desativar(id_inserido)
        # Assert
        assert resultado is True
        obj_db = repo.obter_por_id(id_inserido)
        assert obj_db.ativo is False

    def test_safe_get_valor_existe(self):
        """Testa _safe_get com valor existente"""
        # Arrange
        repo = MockRepo()
        row = {"id": 1, "nome": "Teste"}
        # Act
        valor = repo._safe_get(row, "nome")
        # Assert
        assert valor == "Teste"

    def test_safe_get_valor_none(self):
        """Testa _safe_get com valor None"""
        # Arrange
        repo = MockRepo()
        row = {"id": 1, "nome": None}
        # Act
        valor = repo._safe_get(row, "nome", "Padrão")
        # Assert
        assert valor == "Padrão"

    def test_safe_get_chave_nao_existe(self):
        """Testa _safe_get com chave que não existe (linhas 43-44)"""
        # Arrange
        repo = MockRepo()
        row = {"id": 1}
        # Act
        valor = repo._safe_get(row, "campo_inexistente", "Padrão")
        # Assert
        assert valor == "Padrão"


class TestBaseRepoChaveComposta:
    """Testes para BaseRepoChaveComposta"""

    def test_criar_tabela_composta(self, test_db):
        """Testa criação de tabela com chave composta"""
        # Arrange
        repo = MockCompostaRepo()
        # Act
        resultado = repo.criar_tabela()
        # Assert
        assert resultado is True

    def test_inserir_composta(self, test_db):
        """Testa inserção com chave composta (linhas 309-320)"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        obj = MockCompostaModel(id_a=1, id_b=2, valor="Teste")
        # Act
        resultado = repo.inserir(obj)
        # Assert
        assert resultado is True
        obj_db = repo.obter_por_chave(1, 2)
        assert obj_db.valor == "Teste"

    def test_excluir_composta(self, test_db):
        """Testa exclusão com chave composta (linhas 325-346)"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        obj = MockCompostaModel(id_a=1, id_b=2, valor="Para excluir")
        repo.inserir(obj)
        # Act
        resultado = repo.excluir(1, 2)
        # Assert
        assert resultado is True
        with pytest.raises(RecursoNaoEncontradoError):
            repo.obter_por_chave(1, 2)

    def test_excluir_composta_nao_existe(self, test_db):
        """Testa exclusão com chave composta que não existe (linha 341)"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        # Act
        resultado = repo.excluir(999, 888)
        # Assert
        assert resultado is False

    def test_excluir_composta_valores_insuficientes(self, test_db):
        """Testa exclusão com número incorreto de valores"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(ValidacaoError) as exc_info:
            repo.excluir(1)  # Falta o segundo valor
        assert "Esperado 2 valores" in str(exc_info.value)

    def test_obter_por_chave(self, test_db):
        """Testa obtenção por chave composta (linhas 351-366)"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        obj = MockCompostaModel(id_a=1, id_b=2, valor="Buscar")
        repo.inserir(obj)
        # Act
        obj_db = repo.obter_por_chave(1, 2)
        # Assert
        assert obj_db.valor == "Buscar"

    def test_obter_por_chave_valores_insuficientes(self, test_db):
        """Testa obtenção com número incorreto de valores"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(ValidacaoError) as exc_info:
            repo.obter_por_chave(1)  # Falta o segundo valor
        assert "Esperado 2 valores" in str(exc_info.value)

    def test_obter_por_chave_nao_existe(self, test_db):
        """Testa obtenção de chave que não existe"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        # Act & Assert
        with pytest.raises(RecursoNaoEncontradoError):
            repo.obter_por_chave(999, 888)

    def test_listar_todos_composta(self, test_db):
        """Testa listagem com chave composta (linha 370)"""
        # Arrange
        repo = MockCompostaRepo()
        repo.criar_tabela()
        repo.inserir(MockCompostaModel(id_a=1, id_b=2, valor="Item 1"))
        repo.inserir(MockCompostaModel(id_a=1, id_b=3, valor="Item 2"))
        # Act
        lista = repo.listar_todos()
        # Assert
        assert len(lista) == 2

    def test_init_campos_chave(self, test_db):
        """Testa inicialização com campos_chave (linhas 303-304)"""
        # Arrange & Act
        repo = MockCompostaRepo()
        # Assert
        assert repo.campos_chave == ["id_a", "id_b"]
        assert repo.nome_tabela == "mock_composta"
        assert repo.model_class == MockCompostaModel
