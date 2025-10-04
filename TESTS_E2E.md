# 🧪 Plano de Testes E2E - CaseBem

## 🎯 Visão Geral

Implementar suite completa de testes End-to-End para o sistema CaseBem, cobrindo todos os fluxos de usuário nos 3 perfis (Admin, Fornecedor, Noivo) e funcionalidades públicas.

## 🔧 Ferramenta Recomendada: Playwright + Chrome DevTools MCP

### Por quê Playwright?

- ✅ Você **já tem MCP Chrome DevTools** conectado - podemos usá-lo imediatamente
- ✅ Suporta Python nativamente (seu projeto é Python)
- ✅ Navegação headless/headed para debugging
- ✅ Screenshots e vídeos automáticos de falhas
- ✅ Traços detalhados para debugging
- ✅ Compatível com pytest (sua stack de testes)
- ✅ Auto-waiting inteligente (reduz flakiness)

### Alternativas consideradas

- **Selenium**: Mais verboso, menos moderno, setup complexo
- **Cypress**: JavaScript only, não compatível com Python
- **Puppeteer**: Apenas Chrome, JavaScript only

## 📁 Estrutura Proposta

```
tests/
├── e2e/                                    # Nova pasta de testes E2E
│   ├── __init__.py
│   ├── conftest.py                         # Fixtures compartilhadas
│   ├── helpers/                            # Utilitários E2E
│   │   ├── __init__.py
│   │   ├── navigation.py                   # Helpers de navegação
│   │   ├── assertions.py                   # Asserções customizadas
│   │   └── data_builders.py                # Builders de dados de teste
│   ├── fixtures/                           # Fixtures de dados
│   │   ├── __init__.py
│   │   └── usuarios_fixtures.py            # Usuários para testes
│   ├── test_1_publico.py                   # Área pública (13 testes)
│   ├── test_2_admin.py                     # Fluxos de Admin (10 testes)
│   ├── test_3_fornecedor.py                # Fluxos de Fornecedor (16 testes)
│   ├── test_4_noivo.py                     # Fluxos de Noivo (18 testes)
│   ├── test_5_integracao.py                # Fluxos completos (5 testes)
│   └── screenshots/                        # Screenshots de falhas
└── pyproject.toml                          # Adicionar config Playwright
```

## 🧪 Cobertura de Testes por Perfil

### 1️⃣ Área Pública (test_1_publico.py) - 13 testes

#### Navegação e Visualização
- `test_visualizar_home_page()` - Verifica carregamento da página inicial
- `test_navegacao_sobre()` - Navega e verifica página Sobre
- `test_navegacao_contato()` - Navega e verifica página Contato
- `test_listar_itens_publicos()` - Lista todos os itens públicos disponíveis
- `test_listar_produtos_publicos()` - Filtra e lista apenas produtos
- `test_listar_servicos_publicos()` - Filtra e lista apenas serviços
- `test_listar_espacos_publicos()` - Filtra e lista apenas espaços
- `test_visualizar_detalhes_item()` - Visualiza detalhes completos de um item

#### Cadastro e Autenticação
- `test_cadastro_noivos_completo()` - Preenche e submete formulário de cadastro de casal
- `test_cadastro_fornecedor_completo()` - Preenche e submete formulário de cadastro de fornecedor
- `test_login_como_admin()` - Login com credenciais de administrador
- `test_login_como_fornecedor()` - Login com credenciais de fornecedor
- `test_login_como_noivo()` - Login com credenciais de noivo

#### Validações
- `test_redirecionamento_pos_login()` - Verifica redirecionamento correto por perfil após login
- `test_logout()` - Testa funcionalidade de logout

### 2️⃣ Perfil Admin (test_2_admin.py) - 10 testes

#### Dashboard
- `test_admin_dashboard_estatisticas()` - Visualiza e valida todas as estatísticas do sistema
- `test_admin_dashboard_widgets()` - Verifica presença de todos os widgets

#### Gestão de Usuários
- `test_admin_listar_usuarios()` - Lista todos os usuários do sistema
- `test_admin_buscar_usuarios()` - Busca usuários por termo
- `test_admin_filtrar_usuarios_por_tipo()` - Filtra usuários por perfil (Admin/Noivo/Fornecedor)
- `test_admin_visualizar_detalhes_usuario()` - Visualiza detalhes completos de um usuário
- `test_admin_criar_novo_admin()` - Cria novo administrador do sistema
- `test_admin_ativar_desativar_usuario()` - Alterna status ativo/inativo de usuário

#### Gestão de Fornecedores
- `test_admin_verificar_fornecedor()` - Verifica um fornecedor pendente

#### Gestão de Categorias
- `test_admin_listar_categorias()` - Lista todas as categorias
- `test_admin_criar_categoria()` - Cria nova categoria de produto/serviço
- `test_admin_editar_categoria()` - Edita categoria existente
- `test_admin_ativar_desativar_categoria()` - Alterna status de categoria

#### Gestão de Itens
- `test_admin_listar_itens()` - Lista todos os itens do sistema
- `test_admin_visualizar_item()` - Visualiza detalhes de item
- `test_admin_moderar_item()` - Ativa/desativa item para moderação

#### Perfil
- `test_admin_visualizar_perfil()` - Visualiza perfil do administrador
- `test_admin_editar_perfil()` - Edita dados do perfil
- `test_admin_alterar_senha()` - Altera senha do administrador

### 3️⃣ Perfil Fornecedor (test_3_fornecedor.py) - 16 testes

#### Dashboard
- `test_fornecedor_dashboard_estatisticas()` - Visualiza estatísticas pessoais
- `test_fornecedor_dashboard_itens_recentes()` - Verifica lista de itens recentes no dashboard

#### Gestão de Itens
- `test_fornecedor_listar_meus_itens()` - Lista todos os itens do fornecedor
- `test_fornecedor_criar_produto()` - Cria novo produto
- `test_fornecedor_criar_servico()` - Cria novo serviço
- `test_fornecedor_criar_espaco()` - Cria novo espaço para eventos
- `test_fornecedor_criar_item_com_foto()` - Cria item com upload de foto
- `test_fornecedor_editar_item()` - Edita item existente
- `test_fornecedor_editar_foto_item()` - Atualiza foto de um item
- `test_fornecedor_ativar_desativar_item()` - Alterna status do item
- `test_fornecedor_excluir_item()` - Exclui item e foto associada
- `test_fornecedor_filtrar_itens_por_tipo()` - Filtra itens por tipo (produto/serviço/espaço)
- `test_fornecedor_filtrar_itens_por_status()` - Filtra itens ativos/inativos
- `test_fornecedor_filtrar_itens_por_preco()` - Filtra itens por faixa de preço

#### Gestão de Demandas
- `test_fornecedor_listar_demandas()` - Lista demandas recebidas
- `test_fornecedor_visualizar_demanda()` - Visualiza detalhes de demanda
- `test_fornecedor_filtrar_demandas()` - Filtra demandas por status

#### Gestão de Orçamentos
- `test_fornecedor_propor_orcamento()` - Propõe orçamento para demanda
- `test_fornecedor_listar_orcamentos()` - Lista orçamentos enviados
- `test_fornecedor_visualizar_orcamento()` - Visualiza status de orçamento
- `test_fornecedor_editar_orcamento_pendente()` - Edita orçamento ainda não aceito

#### Perfil
- `test_fornecedor_visualizar_perfil()` - Visualiza perfil do fornecedor
- `test_fornecedor_editar_perfil()` - Edita dados cadastrais
- `test_fornecedor_upload_avatar()` - Faz upload de avatar
- `test_fornecedor_remover_avatar()` - Remove avatar do perfil

### 4️⃣ Perfil Noivo (test_4_noivo.py) - 18 testes

#### Dashboard
- `test_noivo_dashboard_estatisticas()` - Visualiza estatísticas do casal
- `test_noivo_dashboard_demandas_recentes()` - Verifica demandas recentes no dashboard

#### Exploração de Itens
- `test_noivo_listar_produtos()` - Lista produtos disponíveis
- `test_noivo_listar_servicos()` - Lista serviços disponíveis
- `test_noivo_listar_espacos()` - Lista espaços disponíveis
- `test_noivo_buscar_itens()` - Busca itens por termo de pesquisa
- `test_noivo_visualizar_detalhes_item()` - Visualiza detalhes de item específico
- `test_noivo_filtrar_itens_por_categoria()` - Filtra itens por categoria
- `test_noivo_filtrar_itens_por_preco()` - Filtra itens por faixa de preço

#### Gestão de Fornecedores
- `test_noivo_listar_fornecedores()` - Lista fornecedores verificados
- `test_noivo_visualizar_perfil_fornecedor()` - Visualiza perfil público de fornecedor
- `test_noivo_filtrar_fornecedores()` - Filtra fornecedores por tipo

#### Gestão de Demandas
- `test_noivo_criar_demanda()` - Cria nova demanda de casamento
- `test_noivo_listar_demandas()` - Lista demandas do casal
- `test_noivo_visualizar_demanda()` - Visualiza detalhes de demanda
- `test_noivo_editar_demanda()` - Edita demanda existente
- `test_noivo_cancelar_demanda()` - Cancela demanda ativa
- `test_noivo_filtrar_demandas_por_status()` - Filtra demandas (ativa/cancelada/concluída)

#### Gestão de Orçamentos
- `test_noivo_listar_orcamentos()` - Lista orçamentos recebidos
- `test_noivo_visualizar_orcamento()` - Visualiza detalhes de orçamento
- `test_noivo_aceitar_orcamento()` - Aceita orçamento proposto
- `test_noivo_rejeitar_orcamento()` - Rejeita orçamento proposto
- `test_noivo_filtrar_orcamentos_por_status()` - Filtra orçamentos (pendente/aceito/rejeitado)

#### Favoritos
- `test_noivo_adicionar_favorito()` - Adiciona item aos favoritos
- `test_noivo_listar_favoritos()` - Lista todos os favoritos
- `test_noivo_remover_favorito()` - Remove item dos favoritos

#### Checklist
- `test_noivo_visualizar_checklist()` - Visualiza checklist de casamento
- `test_noivo_marcar_item_checklist()` - Marca/desmarca item do checklist

#### Perfil
- `test_noivo_visualizar_perfil()` - Visualiza perfil do casal
- `test_noivo_editar_dados_casal()` - Edita dados do casamento
- `test_noivo_upload_avatar()` - Faz upload de avatar

### 5️⃣ Fluxos Integrados (test_5_integracao.py) - 5 testes

#### Fluxos Completos End-to-End
- `test_fluxo_completo_demanda_orcamento()`
  - Noivo cria demanda
  - Fornecedor visualiza demanda
  - Fornecedor propõe orçamento
  - Noivo recebe notificação
  - Noivo visualiza orçamento
  - Noivo aceita orçamento
  - Status atualizado para ambos

- `test_fluxo_moderacao_item()`
  - Fornecedor cria item
  - Admin recebe para moderação
  - Admin visualiza item
  - Admin aprova item
  - Item aparece publicamente

- `test_fluxo_verificacao_fornecedor()`
  - Fornecedor se cadastra
  - Admin lista fornecedores não verificados
  - Admin verifica fornecedor
  - Status atualizado
  - Fornecedor recebe acesso completo

- `test_fluxo_busca_e_favoritos()`
  - Noivo faz login
  - Noivo busca por termo
  - Noivo visualiza item
  - Noivo adiciona aos favoritos
  - Noivo acessa favoritos
  - Noivo remove dos favoritos

- `test_fluxo_cadastro_login_demanda()`
  - Cadastro completo de noivos
  - Login com credenciais criadas
  - Criação de primeira demanda
  - Logout

## 📦 Dependências a Adicionar

### pyproject.toml

```toml
[project.optional-dependencies]
e2e = [
    "playwright>=1.40.0",
    "pytest-playwright>=0.4.3",
]
```

### Instalação

```bash
# Instalar dependências E2E
pip install -e ".[e2e]"

# Instalar browsers do Playwright
playwright install chromium

# Ou instalar tudo de uma vez
pip install playwright pytest-playwright
playwright install chromium
```

## 🛠️ Configuração Inicial

### 1. tests/e2e/conftest.py

```python
"""
Configuração de fixtures compartilhadas para testes E2E
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from typing import Generator
import os

# URLs base
BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000")

# Credenciais de teste
USUARIOS_TESTE = {
    "admin": {
        "email": "admin@casebem.com",
        "senha": "1234aA@#"
    },
    "fornecedor": {
        "email": "fornecedor@teste.com",
        "senha": "teste123"
    },
    "noivo": {
        "email": "noivo@teste.com",
        "senha": "teste123"
    }
}

@pytest.fixture(scope="session")
def browser(playwright) -> Browser:
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
    page.wait_for_url(f"{BASE_URL}/{perfil}/**")

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """Captura screenshot automático em caso de falha"""
    yield
    if request.node.rep_call.failed:
        screenshot_path = f"tests/e2e/screenshots/{request.node.name}.png"
        page.screenshot(path=screenshot_path)
        print(f"\n📸 Screenshot salvo: {screenshot_path}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar resultado do teste"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
```

### 2. tests/e2e/helpers/navigation.py

```python
"""
Helpers de navegação para testes E2E
"""
from playwright.sync_api import Page
from typing import Dict

def login_as(page: Page, perfil: str, email: str = None, senha: str = None):
    """
    Faz login com perfil específico

    Args:
        page: Página do Playwright
        perfil: 'admin', 'fornecedor' ou 'noivo'
        email: Email customizado (opcional)
        senha: Senha customizada (opcional)
    """
    from tests.e2e.conftest import USUARIOS_TESTE, BASE_URL

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
    from tests.e2e.conftest import BASE_URL
    page.goto(f"{BASE_URL}/{perfil}/dashboard")
    page.wait_for_load_state("networkidle")

def fill_form(page: Page, data: Dict[str, str]):
    """
    Preenche formulário com dados fornecidos

    Args:
        page: Página do Playwright
        data: Dicionário {nome_campo: valor}
    """
    for field, value in data.items():
        selector = f'input[name="{field}"], textarea[name="{field}"], select[name="{field}"]'
        page.fill(selector, str(value))

def wait_for_success_message(page: Page, timeout: int = 5000):
    """Aguarda mensagem de sucesso aparecer"""
    page.wait_for_selector('.alert-success, .toast-success', timeout=timeout)

def wait_for_error_message(page: Page, timeout: int = 5000):
    """Aguarda mensagem de erro aparecer"""
    page.wait_for_selector('.alert-danger, .toast-error', timeout=timeout)

def logout(page: Page):
    """Faz logout do sistema"""
    from tests.e2e.conftest import BASE_URL
    page.goto(f"{BASE_URL}/logout")
    page.wait_for_url(f"{BASE_URL}/")
```

### 3. tests/e2e/helpers/assertions.py

```python
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

def assert_success_message(page: Page, message: str = None):
    """Valida presença de mensagem de sucesso"""
    selector = '.alert-success, .toast-success'
    assert page.is_visible(selector), "Mensagem de sucesso não encontrada"

    if message:
        content = page.text_content(selector)
        assert message in content, f"Mensagem '{message}' não encontrada em '{content}'"

def assert_error_message(page: Page, message: str = None):
    """Valida presença de mensagem de erro"""
    selector = '.alert-danger, .toast-error'
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
```

### 4. tests/e2e/helpers/data_builders.py

```python
"""
Builders de dados para testes E2E
"""
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('pt_BR')

class DemandaBuilder:
    """Builder para criar dados de demanda"""

    @staticmethod
    def build(titulo: str = None, descricao: str = None) -> dict:
        return {
            "titulo": titulo or f"Demanda Teste - {fake.word()}",
            "descricao": descricao or fake.text(200),
            "data_necessaria": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "orcamento_estimado": f"{fake.random_int(500, 5000)}.00"
        }

class ItemBuilder:
    """Builder para criar dados de item"""

    @staticmethod
    def build(tipo: str = "PRODUTO", nome: str = None) -> dict:
        return {
            "tipo": tipo,
            "nome": nome or f"Item Teste - {fake.word()}",
            "descricao": fake.text(150),
            "preco": f"{fake.random_int(50, 1000)}.00",
            "categoria": "1",  # Ajustar conforme categorias disponíveis
            "observacoes": fake.sentence()
        }

class OrcamentoBuilder:
    """Builder para criar dados de orçamento"""

    @staticmethod
    def build(valor: float = None, descricao: str = None) -> dict:
        return {
            "valor": valor or f"{fake.random_int(1000, 10000)}.00",
            "descricao": descricao or fake.text(200),
            "prazo_entrega": f"{fake.random_int(7, 30)} dias",
            "forma_pagamento": fake.random_element(["À vista", "Parcelado", "Entrada + Saldo"])
        }

class NoivosBuilder:
    """Builder para cadastro de noivos"""

    @staticmethod
    def build() -> dict:
        senha = "Teste@123"
        return {
            # Noivo 1
            "nome1": fake.name(),
            "email1": fake.email(),
            "telefone1": fake.phone_number(),
            "cpf1": fake.cpf(),
            "data_nascimento1": fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
            "genero1": fake.random_element(["Masculino", "Feminino", "Outro"]),

            # Noivo 2
            "nome2": fake.name(),
            "email2": fake.email(),
            "telefone2": fake.phone_number(),
            "cpf2": fake.cpf(),
            "data_nascimento2": fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
            "genero2": fake.random_element(["Masculino", "Feminino", "Outro"]),

            # Dados do casamento
            "data_casamento": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
            "local_previsto": fake.city(),
            "orcamento": f"{fake.random_int(10000, 50000)}.00",
            "numero_convidados": str(fake.random_int(50, 300)),

            # Senha
            "senha": senha,
            "confirmar_senha": senha
        }

class FornecedorBuilder:
    """Builder para cadastro de fornecedor"""

    @staticmethod
    def build(tipo: str = "PRODUTO") -> dict:
        senha = "Teste@123"
        return {
            "nome": fake.company(),
            "email": fake.email(),
            "telefone": fake.phone_number(),
            "cnpj": fake.cnpj(),
            "tipo_fornecimento": tipo,
            "descricao": fake.text(200),
            "endereco": fake.address(),
            "cidade": fake.city(),
            "estado": fake.estado_sigla(),
            "senha": senha,
            "confirmar_senha": senha
        }
```

## 🎬 Exemplo de Teste Completo

### tests/e2e/test_5_integracao.py

```python
"""
Testes de integração E2E - Fluxos completos
"""
import pytest
from playwright.sync_api import Page
from tests.e2e.helpers.navigation import login_as, goto_dashboard, fill_form, logout
from tests.e2e.helpers.assertions import (
    assert_url_contains,
    assert_success_message,
    assert_element_visible
)
from tests.e2e.helpers.data_builders import DemandaBuilder, OrcamentoBuilder

def test_fluxo_completo_demanda_orcamento(browser):
    """
    Testa fluxo completo:
    1. Noivo cria demanda
    2. Fornecedor visualiza demanda
    3. Fornecedor propõe orçamento
    4. Noivo visualiza orçamento
    5. Noivo aceita orçamento
    """

    # === PASSO 1: Noivo cria demanda ===
    page_noivo = browser.new_page()
    login_as(page_noivo, 'noivo')
    goto_dashboard(page_noivo, 'noivo')

    # Navegar para criar demanda
    page_noivo.click("text=Nova Demanda")
    assert_url_contains(page_noivo, "/noivo/demandas/nova")

    # Preencher e submeter
    demanda_data = DemandaBuilder.build(
        titulo="Fotógrafo Profissional",
        descricao="Necessito de fotógrafo para casamento dia 15/06"
    )
    fill_form(page_noivo, demanda_data)
    page_noivo.click("button:has-text('Criar Demanda')")

    # Validar sucesso
    assert_success_message(page_noivo, "Demanda criada")
    assert_url_contains(page_noivo, "/noivo/demandas")

    # Validar demanda na listagem
    assert_element_visible(page_noivo, f"text={demanda_data['titulo']}")

    # === PASSO 2: Fornecedor visualiza demanda ===
    page_forn = browser.new_page()
    login_as(page_forn, 'fornecedor')
    goto_dashboard(page_forn, 'fornecedor')

    # Navegar para demandas
    page_forn.click("text=Demandas")
    assert_url_contains(page_forn, "/fornecedor/demandas")

    # Localizar e abrir demanda criada
    page_forn.click(f"text={demanda_data['titulo']}")
    assert_element_visible(page_forn, f"text={demanda_data['descricao']}")

    # === PASSO 3: Fornecedor propõe orçamento ===
    page_forn.click("text=Propor Orçamento")
    assert_url_contains(page_forn, "/fornecedor/orcamentos/propor")

    # Preencher orçamento
    orcamento_data = OrcamentoBuilder.build(
        valor="2500.00",
        descricao="Pacote completo com 8h de cobertura"
    )
    fill_form(page_forn, orcamento_data)
    page_forn.click("button:has-text('Enviar Orçamento')")

    # Validar sucesso
    assert_success_message(page_forn, "Orçamento enviado")

    # === PASSO 4: Noivo visualiza orçamento ===
    page_noivo.click("text=Orçamentos")
    page_noivo.reload()  # Recarregar para ver novo orçamento

    # Localizar orçamento
    assert_element_visible(page_noivo, f"text={demanda_data['titulo']}")
    assert_element_visible(page_noivo, "text=R$ 2.500,00")

    # Abrir detalhes
    page_noivo.click(f"text={demanda_data['titulo']}")
    assert_element_visible(page_noivo, f"text={orcamento_data['descricao']}")

    # === PASSO 5: Noivo aceita orçamento ===
    page_noivo.click("button:has-text('Aceitar Orçamento')")

    # Confirmar modal se houver
    if page_noivo.is_visible("button:has-text('Confirmar')"):
        page_noivo.click("button:has-text('Confirmar')")

    # Validar sucesso
    assert_success_message(page_noivo, "Orçamento aceito")
    assert_element_visible(page_noivo, "text=Aceito")

    # === VALIDAÇÃO FINAL: Status atualizado para fornecedor ===
    page_forn.click("text=Orçamentos")
    page_forn.reload()
    assert_element_visible(page_forn, "text=Aceito")

    # Cleanup
    page_noivo.close()
    page_forn.close()
```

## 📊 Métricas de Sucesso

### Objetivos

- ✅ **Cobertura**: 100% dos 102 endpoints testados
- ✅ **Estabilidade**: 95%+ taxa de sucesso (max 5% flakiness)
- ✅ **Performance**: Cada teste < 10s, suite completa < 15min
- ✅ **Relatórios**: HTML report com screenshots de falhas
- ✅ **CI/CD Ready**: Executar em pipeline automatizado

### Comandos de Execução

```bash
# Executar todos os testes E2E
pytest tests/e2e/ -v

# Executar testes específicos
pytest tests/e2e/test_1_publico.py -v

# Executar com relatório HTML
pytest tests/e2e/ --html=report.html --self-contained-html

# Executar em modo headed (ver navegador)
pytest tests/e2e/ --headed

# Executar com paralelização
pytest tests/e2e/ -n 4

# Executar com slowmo (útil para debugging)
pytest tests/e2e/ --slowmo 1000

# Executar apenas testes de integração
pytest tests/e2e/test_5_integracao.py -v
```

## 📅 Plano de Implementação

### Fase 1: Setup (2h)
1. ✅ Instalar Playwright e pytest-playwright
2. ✅ Criar estrutura de pastas tests/e2e/
3. ✅ Configurar conftest.py com fixtures
4. ✅ Criar helpers básicos (navigation, assertions, data_builders)
5. ✅ Testar configuração básica

### Fase 2: Testes Públicos (2h)
6. ✅ Implementar test_1_publico.py (13 testes)
7. ✅ Validar navegação e cadastros

### Fase 3: Testes Admin (3h)
8. ✅ Implementar test_2_admin.py (10 testes)
9. ✅ Validar gestão de usuários, categorias e verificação

### Fase 4: Testes Fornecedor (4h)
10. ✅ Implementar test_3_fornecedor.py (16 testes)
11. ✅ Validar gestão de itens, demandas e orçamentos

### Fase 5: Testes Noivo (4h)
12. ✅ Implementar test_4_noivo.py (18 testes)
13. ✅ Validar exploração, demandas, orçamentos e favoritos

### Fase 6: Testes Integração (3h)
14. ✅ Implementar test_5_integracao.py (5 fluxos completos)
15. ✅ Validar fluxos end-to-end completos

### Fase 7: Refinamento (2h)
16. ✅ Adicionar relatórios HTML customizados
17. ✅ Configurar screenshots automáticos em falhas
18. ✅ Documentação de uso e manutenção
19. ✅ Otimização de performance

**Total estimado: 20 horas** (~62 testes E2E completos)

## ✅ Vantagens da Abordagem

1. **✅ Usa MCP já conectado** - Chrome DevTools MCP disponível
2. **✅ Python nativo** - Mesma linguagem do projeto
3. **✅ Integra com pytest** - Mesma ferramenta dos testes atuais (135 testes unitários)
4. **✅ Auto-waiting** - Playwright aguarda elementos automaticamente (testes mais estáveis)
5. **✅ Screenshots/videos** - Debugging facilitado com capturas automáticas
6. **✅ Parallelização** - Execução rápida com pytest-xdist
7. **✅ Multi-browser** - Suporta Chromium, Firefox, WebKit
8. **✅ Documentação rica** - API bem documentada e comunidade ativa

## 🔄 Manutenção Contínua

### Boas Práticas

1. **Executar antes de cada commit**: `pytest tests/e2e/ --maxfail=3`
2. **Atualizar testes ao modificar features**: Manter sincronizado
3. **Review de testes em PRs**: Validar cobertura de novos endpoints
4. **Monitorar flakiness**: Identificar e corrigir testes instáveis
5. **Atualizar dados de teste**: Manter fixtures atualizadas

### CI/CD Integration

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[e2e]"
          playwright install chromium

      - name: Start application
        run: |
          python main.py &
          sleep 5

      - name: Run E2E tests
        run: pytest tests/e2e/ --html=report.html --self-contained-html

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-report
          path: report.html
```

## 📚 Referências

- [Playwright Python Docs](https://playwright.dev/python/docs/intro)
- [pytest-playwright Plugin](https://github.com/microsoft/playwright-pytest)
- [Best Practices E2E Testing](https://playwright.dev/python/docs/best-practices)
- [Chrome DevTools MCP](https://github.com/anthropics/mcp-chrome-devtools)

---

**Status**: 📋 Planejamento completo - Aguardando implementação

**Versão**: 1.0

**Última Atualização**: Outubro 2025
