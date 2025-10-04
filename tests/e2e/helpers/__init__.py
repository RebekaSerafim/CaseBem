"""
Helpers e utilitários para testes E2E
"""
from .assertions import (
    assert_url_contains,
    assert_url_equals,
    assert_element_visible,
    assert_element_hidden,
    assert_element_count,
    assert_success_message,
)

from .navigation import (
    login_as,
    goto_dashboard,
    fill_form,
)

from .data_builders import (
    DemandaBuilder,
    ItemBuilder,
    OrcamentoBuilder,
    CategoriaBuilder,
    NoivosBuilder,
    FornecedorBuilder,
)

__all__ = [
    # Assertions
    'assert_url_contains',
    'assert_url_equals',
    'assert_element_visible',
    'assert_element_hidden',
    'assert_element_count',
    'assert_success_message',
    # Navigation
    'login_as',
    'goto_dashboard',
    'fill_form',
    # Builders
    'DemandaBuilder',
    'ItemBuilder',
    'OrcamentoBuilder',
    'CategoriaBuilder',
    'NoivosBuilder',
    'FornecedorBuilder',
]
