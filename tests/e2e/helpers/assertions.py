"""
Asserções customizadas para testes E2E
"""
from playwright.sync_api import Page

def assert_url_contains(page: Page, text: str):
    """Valida que URL atual contém texto"""
    assert text in page.url, f"URL '{page.url}' não contém '{text}'"

def assert_url_equals(page: Page, url: str):
    """Valida que URL atual é exatamente igual"""
    assert page.url == url, f"URL '{page.url}' diferente de '{url}'"

def assert_element_visible(page: Page, selector: str):
    """Valida que elemento está visível"""
    assert page.is_visible(selector), f"Elemento '{selector}' não está visível"

def assert_element_hidden(page: Page, selector: str):
    """Valida que elemento está oculto"""
    assert not page.is_visible(selector), f"Elemento '{selector}' está visível"

def assert_element_count(page: Page, selector: str, count: int):
    """Valida número de elementos que correspondem ao seletor"""
    actual_count = page.locator(selector).count()
    assert actual_count == count, f"Esperado {count} elementos, encontrado {actual_count}"

def assert_success_message(page: Page, message: str = None):
    """Valida presença de mensagem de sucesso"""
    selector = '.alert-success, .toast-success, [class*="success"]'
    assert page.is_visible(selector), "Mensagem de sucesso não encontrada"

    if message:
        content = page.text_content(selector)
        assert message in content, f"Mensagem '{message}' não encontrada em '{content}'"

def assert_error_message(page: Page, message: str = None):
    """Valida presença de mensagem de erro"""
    selector = '.alert-danger, .toast-error, [class*="error"]'
    assert page.is_visible(selector), "Mensagem de erro não encontrada"

    if message:
        content = page.text_content(selector)
        assert message in content, f"Mensagem '{message}' não encontrada em '{content}'"

def assert_table_row_count(page: Page, selector: str, count: int):
    """Valida número de linhas em tabela"""
    rows = page.query_selector_all(selector)
    assert len(rows) == count, f"Esperado {count} linhas, encontrado {len(rows)}"

def assert_table_has_text(page: Page, selector: str, text: str):
    """Valida que tabela contém texto"""
    content = page.text_content(selector)
    assert text in content, f"Texto '{text}' não encontrado na tabela"

def assert_text_visible(page: Page, text: str):
    """Valida que texto está visível na página"""
    selector = f'text={text}'
    assert page.is_visible(selector), f"Texto '{text}' não encontrado na página"

def assert_heading_visible(page: Page, text: str):
    """Valida que cabeçalho com texto está visível"""
    selector = f'h1:has-text("{text}"), h2:has-text("{text}"), h3:has-text("{text}")'
    assert page.locator(selector).count() > 0, f"Cabeçalho '{text}' não encontrado"
