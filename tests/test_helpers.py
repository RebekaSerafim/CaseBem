"""
Utilitários para facilitar escrita de testes
"""

from typing import Any, Dict, List
from contextlib import contextmanager
import pytest


@contextmanager
def nao_deve_gerar_erro():
    """Context manager para garantir que não há erros"""
    try:
        yield
    except Exception as e:
        pytest.fail(f"Não deveria gerar erro, mas gerou: {e}")


def assert_objeto_possui_atributos(objeto: Any, atributos: Dict[str, Any]):
    """Verifica se objeto possui os atributos esperados"""
    for nome_attr, valor_esperado in atributos.items():
        assert hasattr(objeto, nome_attr), f"Objeto não possui atributo '{nome_attr}'"
        valor_atual = getattr(objeto, nome_attr)
        assert valor_atual == valor_esperado, f"Atributo '{nome_attr}': esperado {valor_esperado}, obtido {valor_atual}"


def assert_listas_equivalentes(lista1: List[Any], lista2: List[Any], comparar_por: str = 'id'):
    """Compara listas de objetos por um atributo específico"""
    ids1 = [getattr(obj, comparar_por) for obj in lista1]
    ids2 = [getattr(obj, comparar_por) for obj in lista2]
    assert set(ids1) == set(ids2), f"Listas não são equivalentes: {ids1} != {ids2}"


def assert_usuario_valido(usuario):
    """Verifica se um usuário tem atributos básicos válidos"""
    assert hasattr(usuario, 'nome'), "Usuário deve ter nome"
    assert hasattr(usuario, 'email'), "Usuário deve ter email"
    assert hasattr(usuario, 'perfil'), "Usuário deve ter perfil"
    assert len(usuario.nome) > 0, "Nome não pode ser vazio"
    assert '@' in usuario.email, "Email deve ter formato válido"


def assert_fornecedor_valido(fornecedor):
    """Verifica se um fornecedor tem atributos básicos válidos"""
    assert_usuario_valido(fornecedor)  # Fornecedor herda de usuário
    assert hasattr(fornecedor, 'nome_empresa'), "Fornecedor deve ter nome_empresa"
    assert hasattr(fornecedor, 'verificado'), "Fornecedor deve ter status de verificado"


def assert_categoria_valida(categoria):
    """Verifica se uma categoria tem atributos básicos válidos"""
    assert hasattr(categoria, 'nome'), "Categoria deve ter nome"
    assert hasattr(categoria, 'tipo_fornecimento'), "Categoria deve ter tipo_fornecimento"
    assert hasattr(categoria, 'ativo'), "Categoria deve ter status ativo"
    assert len(categoria.nome) > 0, "Nome da categoria não pode ser vazio"


def assert_item_valido(item):
    """Verifica se um item tem atributos básicos válidos"""
    assert hasattr(item, 'nome'), "Item deve ter nome"
    assert hasattr(item, 'preco'), "Item deve ter preço"
    assert hasattr(item, 'id_fornecedor'), "Item deve ter id_fornecedor"
    assert len(item.nome) > 0, "Nome do item não pode ser vazio"
    assert item.preco >= 0, "Preço deve ser não negativo"


def assert_casal_valido(casal):
    """Verifica se um casal tem atributos básicos válidos"""
    assert hasattr(casal, 'id_noivo1'), "Casal deve ter id_noivo1"
    assert hasattr(casal, 'id_noivo2'), "Casal deve ter id_noivo2"
    assert hasattr(casal, 'data_casamento'), "Casal deve ter data_casamento"
    assert casal.id_noivo1 != casal.id_noivo2, "Noivos devem ser diferentes"


class AssertHelper:
    """Classe com métodos auxiliares para assertions mais complexas"""

    @staticmethod
    def lista_nao_vazia(lista: List[Any], nome_lista: str = "lista"):
        """Verifica se a lista não está vazia"""
        assert isinstance(lista, list), f"{nome_lista} deve ser uma lista"
        assert len(lista) > 0, f"{nome_lista} não pode estar vazia"

    @staticmethod
    def todos_elementos_sao_tipo(lista: List[Any], tipo_esperado: type, nome_lista: str = "lista"):
        """Verifica se todos elementos da lista são do tipo esperado"""
        AssertHelper.lista_nao_vazia(lista, nome_lista)
        for i, elemento in enumerate(lista):
            assert isinstance(elemento, tipo_esperado), f"Elemento {i} de {nome_lista} deve ser do tipo {tipo_esperado.__name__}"

    @staticmethod
    def ids_unicos(lista: List[Any], nome_lista: str = "lista"):
        """Verifica se todos os IDs da lista são únicos"""
        AssertHelper.lista_nao_vazia(lista, nome_lista)
        ids = [getattr(obj, 'id', None) for obj in lista]
        ids_nao_nulos = [id for id in ids if id is not None]
        assert len(ids_nao_nulos) == len(set(ids_nao_nulos)), f"IDs em {nome_lista} devem ser únicos"

    @staticmethod
    def emails_unicos(lista: List[Any], nome_lista: str = "lista"):
        """Verifica se todos os emails da lista são únicos"""
        AssertHelper.lista_nao_vazia(lista, nome_lista)
        emails = [getattr(obj, 'email', None) for obj in lista]
        emails_nao_nulos = [email for email in emails if email is not None]
        assert len(emails_nao_nulos) == len(set(emails_nao_nulos)), f"Emails em {nome_lista} devem ser únicos"