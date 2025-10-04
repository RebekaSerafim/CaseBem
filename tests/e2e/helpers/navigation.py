"""
Helpers de navegação para testes E2E
"""
from playwright.sync_api import Page
from typing import Dict

# Import conftest constants
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from conftest import USUARIOS_TESTE, BASE_URL

def login_as(page: Page, perfil: str, email: str = None, senha: str = None):
    """
    Faz login com perfil específico

    Args:
        page: Página do Playwright
        perfil: 'admin', 'fornecedor' ou 'noivo'
        email: Email customizado (opcional)
        senha: Senha customizada (opcional)
    """
    creds = USUARIOS_TESTE[perfil]
    email = email or creds["email"]
    senha = senha or creds["senha"]

    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="email"]', email)
    page.fill('input[name="senha"]', senha)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")

def goto_dashboard(page: Page, perfil: str):
    """Navega para o dashboard do perfil"""
    page.goto(f"{BASE_URL}/{perfil}/dashboard")
    page.wait_for_load_state("networkidle")

def fill_form(page: Page, data: Dict[str, str], wait_for_validation: bool = True):
    """
    Preenche formulário com dados fornecidos

    Args:
        page: Página do Playwright
        data: Dicionário {nome_campo: valor}
        wait_for_validation: Se deve aguardar validações JavaScript após cada campo
    """
    for field, value in data.items():
        selector = f'input[name="{field}"], textarea[name="{field}"], select[name="{field}"]'

        # Verificar se elemento existe antes de preencher
        if page.locator(selector).count() > 0:
            element = page.locator(selector).first

            # Verificar tipo de elemento
            tag_name = element.evaluate("el => el.tagName.toLowerCase()")
            input_type = element.evaluate("el => el.type") if tag_name == "input" else None

            if tag_name == "select":
                # Para select, tentar selecionar por valor ou por índice
                try:
                    element.select_option(str(value))
                except:
                    # Se falhar, selecionar primeira opção válida (não vazia)
                    options = element.evaluate("""
                        el => Array.from(el.options)
                            .filter(opt => opt.value && opt.value !== '')
                            .map(opt => opt.value)
                    """)
                    if options and len(options) > 0:
                        element.select_option(options[0])
            elif input_type == "radio":
                # Para radio buttons, procurar pelo value específico
                radio_selector = f'input[name="{field}"][value="{str(value).lower()}"]'
                if page.locator(radio_selector).count() > 0:
                    page.locator(radio_selector).first.click()
                else:
                    # Tentar apenas pelo nome e clicar no primeiro
                    page.locator(f'input[name="{field}"]').first.click()
            elif input_type == "checkbox":
                # Para checkboxes, fazer check
                if str(value).lower() in ['true', '1', 'yes', 'sim']:
                    element.check()
                else:
                    element.uncheck()
            else:
                # Text, email, password, textarea, etc
                element.fill(str(value))

                # Aguardar validações JavaScript (debounce)
                if wait_for_validation:
                    page.wait_for_timeout(300)

def wait_for_success_message(page: Page, timeout: int = 5000):
    """Aguarda mensagem de sucesso aparecer"""
    page.wait_for_selector('.alert-success, .toast-success, [class*="success"]', timeout=timeout)

def wait_for_error_message(page: Page, timeout: int = 5000):
    """Aguarda mensagem de erro aparecer"""
    page.wait_for_selector('.alert-danger, .toast-error, [class*="error"]', timeout=timeout)

def logout(page: Page):
    """Faz logout do sistema"""
    page.goto(f"{BASE_URL}/logout")
    page.wait_for_url(f"{BASE_URL}/")
