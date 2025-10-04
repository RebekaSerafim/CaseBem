"""
Teste de validação da configuração E2E

Este arquivo contém testes básicos para validar que o setup E2E está funcionando corretamente.
"""
import pytest
from playwright.sync_api import Page
from tests.e2e.helpers.navigation import login_as, goto_dashboard, logout
from tests.e2e.helpers.assertions import (
    assert_url_contains,
    assert_text_visible,
    assert_element_visible
)

@pytest.mark.e2e
def test_home_page_loads(page: Page):
    """Valida que a página inicial carrega corretamente"""
    # A página já foi navegada para a home pelo fixture
    assert page.title(), "Página deve ter um título"
    assert_url_contains(page, "localhost:8000")

@pytest.mark.e2e
def test_can_navigate_to_login(page: Page):
    """Valida navegação para página de login"""
    page.click('a[href="/login"]')
    assert_url_contains(page, "/login")

    # Verificar elementos do formulário de login
    assert_element_visible(page, 'input[name="email"]')
    assert_element_visible(page, 'input[name="senha"]')
    assert_element_visible(page, 'button[type="submit"]')

@pytest.mark.e2e
def test_login_as_admin(page: Page):
    """Valida login como administrador"""
    login_as(page, "admin")

    # Deve redirecionar para dashboard do admin
    assert_url_contains(page, "/admin")

@pytest.mark.e2e
def test_login_as_fornecedor(page: Page):
    """Valida login como fornecedor"""
    login_as(page, "fornecedor")

    # Deve redirecionar para dashboard do fornecedor
    assert_url_contains(page, "/fornecedor")

@pytest.mark.e2e
def test_login_as_noivo(page: Page):
    """Valida login como noivo"""
    login_as(page, "noivo")

    # Deve redirecionar para dashboard do noivo
    assert_url_contains(page, "/noivo")

@pytest.mark.e2e
def test_logout_functionality(page: Page):
    """Valida funcionalidade de logout"""
    # Fazer login
    login_as(page, "admin")
    assert_url_contains(page, "/admin")

    # Fazer logout
    logout(page)
    assert_url_contains(page, "localhost:8000")

    # Tentar acessar área restrita deve redirecionar para login
    page.goto("http://localhost:8000/admin/dashboard")
    # Deve redirecionar para login (com ou sem redirect parameter)
    assert "/login" in page.url, f"Deveria redirecionar para login, mas está em: {page.url}"

@pytest.mark.e2e
def test_fixtures_admin_authenticated(page_admin: Page):
    """Valida que a fixture page_admin já está autenticada"""
    # Fixture deve já ter feito login
    assert_url_contains(page_admin, "/admin")

@pytest.mark.e2e
def test_fixtures_fornecedor_authenticated(page_fornecedor: Page):
    """Valida que a fixture page_fornecedor já está autenticada"""
    # Fixture deve já ter feito login
    assert_url_contains(page_fornecedor, "/fornecedor")

@pytest.mark.e2e
def test_fixtures_noivo_authenticated(page_noivo: Page):
    """Valida que a fixture page_noivo já está autenticada"""
    # Fixture deve já ter feito login
    assert_url_contains(page_noivo, "/noivo")
