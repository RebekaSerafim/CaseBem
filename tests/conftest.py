"""
Configurações e fixtures básicas para testes.
Factories específicas estão em tests/factories.py
"""

import pytest
import os
import sys
import tempfile
from typing import Dict, Any

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.factories import (
    UsuarioFactory, FornecedorFactory, CategoriaFactory,
    ItemFactory, CasalFactory, DemandaFactory, OrcamentoFactory, TestDataBuilder
)


@pytest.fixture
def test_db():
    """Cria um banco de dados temporário para testes"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path

    yield db_path

    # Cleanup
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def usuario_factory():
    """Factory para criar usuários nos testes"""
    return UsuarioFactory


@pytest.fixture
def fornecedor_factory():
    """Factory para criar fornecedores nos testes"""
    return FornecedorFactory


@pytest.fixture
def categoria_factory():
    """Factory para criar categorias nos testes"""
    return CategoriaFactory


@pytest.fixture
def item_factory():
    """Factory para criar itens nos testes"""
    return ItemFactory


@pytest.fixture
def casal_factory():
    """Factory para criar casais nos testes"""
    return CasalFactory


@pytest.fixture
def test_data_builder():
    """Builder para criar conjuntos completos de dados"""
    return TestDataBuilder


@pytest.fixture
def dados_completos_teste(test_data_builder):
    """Conjunto completo de dados para testes de integração"""
    return test_data_builder.com_usuarios(5).com_fornecedores(3).com_categorias(5).com_itens(10).construir()


# Fixtures de conveniência (para compatibilidade com testes existentes)
@pytest.fixture
def usuario_exemplo(usuario_factory):
    """Usuário exemplo para compatibilidade"""
    return usuario_factory.criar()


@pytest.fixture
def admin_exemplo(usuario_factory):
    """Admin exemplo para compatibilidade"""
    return usuario_factory.criar_admin()


@pytest.fixture
def lista_usuarios_exemplo(usuario_factory):
    """Lista de usuários para compatibilidade"""
    return usuario_factory.criar_lista(10)


@pytest.fixture
def lista_noivos_exemplo(usuario_factory):
    """Lista de noivos para compatibilidade"""
    return usuario_factory.criar_lista(10, perfil='NOIVO')


@pytest.fixture
def fornecedor_exemplo(fornecedor_factory):
    """Fornecedor exemplo para compatibilidade"""
    return fornecedor_factory.criar()


@pytest.fixture
def lista_fornecedores_exemplo(fornecedor_factory):
    """Lista de fornecedores para compatibilidade"""
    return fornecedor_factory.criar_lista(5)


@pytest.fixture
def categoria_exemplo(categoria_factory):
    """Categoria exemplo para compatibilidade"""
    return categoria_factory.criar()


@pytest.fixture
def lista_categorias_exemplo(categoria_factory):
    """Lista de categorias para compatibilidade"""
    return categoria_factory.criar_lista(5)


@pytest.fixture
def item_exemplo(item_factory):
    """Item exemplo para compatibilidade"""
    return item_factory.criar()


@pytest.fixture
def lista_itens_exemplo(item_factory):
    """Lista de itens para compatibilidade"""
    return item_factory.criar_lista(10)


@pytest.fixture
def casal_exemplo(casal_factory):
    """Casal exemplo para compatibilidade"""
    return casal_factory.criar()


@pytest.fixture
def lista_casais_exemplo(casal_factory):
    """Lista de casais para compatibilidade"""
    return casal_factory.criar_lista(3)


@pytest.fixture
def demanda_factory():
    """Factory para criar demandas nos testes"""
    return DemandaFactory


@pytest.fixture
def orcamento_factory():
    """Factory para criar orçamentos nos testes"""
    return OrcamentoFactory


@pytest.fixture
def demanda_exemplo(demanda_factory):
    """Demanda exemplo para compatibilidade"""
    return demanda_factory.criar()


@pytest.fixture
def lista_demandas_exemplo(demanda_factory):
    """Lista de demandas para compatibilidade"""
    return demanda_factory.criar_lista(5)


@pytest.fixture
def orcamento_exemplo(orcamento_factory):
    """Orçamento exemplo para compatibilidade"""
    return orcamento_factory.criar()


@pytest.fixture
def lista_orcamentos_exemplo(orcamento_factory):
    """Lista de orçamentos para compatibilidade"""
    return orcamento_factory.criar_lista(5)