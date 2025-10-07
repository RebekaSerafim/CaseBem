"""
Configuração de fixtures compartilhadas para testes E2E
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from typing import Generator
import os

# URLs base
# Para configurar uma URL customizada, defina a variável de ambiente E2E_BASE_URL
# Exemplo: export E2E_BASE_URL="http://localhost:3000"
# Exemplo: export E2E_BASE_URL="https://staging.casebem.com"
BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8001")

# Credenciais de teste
# IMPORTANTE: Estes usuários devem existir no banco de dados (via seeds ou criação manual)
USUARIOS_TESTE = {
    "admin": {
        "email": "admin@casebem.com",
        "senha": "1234aA@#"
    },
    "fornecedor": {
        "email": "ana@casamentosperfeitos.com",  # Fornecedor ID 2 do seed
        "senha": "1234aA@#"
    },
    "noivo": {
        "email": "joao.silva@email.com",  # Noivo ID 12 do seed
        "senha": "1234aA@#"
    }
}

@pytest.fixture(scope="session")
def browser(playwright) -> Generator[Browser, None, None]:
    """Browser compartilhado para toda a sessão de testes"""
    browser = playwright.chromium.launch(
        headless=True,  # Mudar para False para ver o navegador
        slow_mo=50  # Delay entre ações para melhor visualização
    )
    yield browser
    browser.close()

@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Contexto isolado para cada teste"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="pt-BR",
        timezone_id="America/Sao_Paulo"
    )
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Página para cada teste"""
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()

@pytest.fixture
def page_admin(context: BrowserContext) -> Generator[Page, None, None]:
    """Página autenticada como Admin"""
    page = context.new_page()
    page.goto(BASE_URL)
    _fazer_login(page, "admin")
    yield page
    page.close()

@pytest.fixture
def page_fornecedor(context: BrowserContext) -> Generator[Page, None, None]:
    """Página autenticada como Fornecedor"""
    page = context.new_page()
    page.goto(BASE_URL)
    _fazer_login(page, "fornecedor")
    yield page
    page.close()

@pytest.fixture
def page_noivo(context: BrowserContext) -> Generator[Page, None, None]:
    """Página autenticada como Noivo"""
    page = context.new_page()
    page.goto(BASE_URL)
    _fazer_login(page, "noivo")
    yield page
    page.close()

def _fazer_login(page: Page, perfil: str):
    """Helper para fazer login"""
    creds = USUARIOS_TESTE[perfil]

    # Navegar para login
    page.goto(f"{BASE_URL}/login")

    # Preencher formulário
    page.fill('input[name="email"]', creds["email"])
    page.fill('input[name="senha"]', creds["senha"])

    # Submeter
    page.click('button[type="submit"]')

    # Aguardar redirecionamento
    page.wait_for_url(f"{BASE_URL}/{perfil}/**", timeout=10000)

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """Captura screenshot automático em caso de falha"""
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_dir = "/Volumes/Externo/Ifes/CaseBem/tests/e2e/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = f"{screenshot_dir}/{request.node.name}.png"
        page.screenshot(path=screenshot_path)
        print(f"\n📸 Screenshot salvo: {screenshot_path}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar resultado do teste"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
