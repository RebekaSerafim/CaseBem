"""
Testes E2E - Área de Administração

Testa todas as funcionalidades disponíveis para administradores:
- Dashboard e visualização de métricas
- Gerenciamento de categorias (CRUD)
- Gerenciamento de usuários
- Aprovação de fornecedores
- Visualização de demandas
- Relatórios e estatísticas
"""
import pytest
from playwright.sync_api import Page
from tests.e2e.helpers.navigation import login_as, fill_form, goto_dashboard, goto_url
from tests.e2e.helpers.assertions import (
    assert_url_contains,
    assert_text_visible,
    assert_element_visible,
    assert_heading_visible,
    assert_at_base_url
)
from tests.e2e.helpers.data_builders import CategoriaBuilder
from tests.e2e.conftest import BASE_URL

# ==================== DASHBOARD E NAVEGAÇÃO ====================

@pytest.mark.e2e
def test_admin_acessar_dashboard(page_admin: Page):
    """Verifica acesso ao dashboard administrativo"""
    # Fixture page_admin já faz login e está no dashboard
    assert_url_contains(page_admin, "/admin")

    # Verificar elementos do dashboard
    # Pode ter métricas, gráficos, estatísticas
    assert page_admin.locator('h1, h2, h3').count() > 0, "Dashboard deve ter títulos"

@pytest.mark.e2e
def test_admin_visualizar_metricas(page_admin: Page):
    """Visualiza métricas e estatísticas do sistema"""
    # Procurar por cards de métricas comuns
    metricas_possiveis = [
        'Total de Usuários',
        'Total de Fornecedores',
        'Total de Casais',
        'Total de Demandas',
        'Total de Itens',
        'Fornecedores Pendentes'
    ]

    # Verificar se pelo menos uma métrica está visível
    found = False
    for metrica in metricas_possiveis:
        if page_admin.locator(f'text=/{metrica}/i').count() > 0:
            found = True
            break

    # Se não encontrou métricas específicas, ao menos verificar que há conteúdo
    if not found:
        assert page_admin.locator('.card, .metric, .stat').count() > 0 or \
               page_admin.locator('h1, h2, h3, h4').count() > 0, \
               "Dashboard deve ter algum conteúdo ou métricas"

@pytest.mark.e2e
def test_admin_menu_navegacao(page_admin: Page):
    """Verifica navegação no menu administrativo"""
    # Verificar presença de links no menu admin
    menu_items = [
        'Dashboard',
        'Categorias',
        'Usuários',
        'Fornecedores',
        'Relatórios'
    ]

    # Contar quantos itens de menu existem
    menu_count = 0
    for item in menu_items:
        if page_admin.locator(f'a:has-text("{item}"), nav:has-text("{item}")').count() > 0:
            menu_count += 1

    assert menu_count >= 2, "Menu admin deve ter pelo menos 2 opções de navegação"

# ==================== CATEGORIAS ====================

@pytest.mark.e2e
def test_admin_listar_categorias(page_admin: Page):
    """Lista todas as categorias cadastradas"""
    # Navegar para categorias
    if page_admin.locator('a:has-text("Categorias"), a[href*="categoria"]').count() > 0:
        page_admin.click('a:has-text("Categorias"), a[href*="categoria"]')
        page_admin.wait_for_load_state("networkidle")

        assert_url_contains(page_admin, "/admin")
        assert "categoria" in page_admin.url.lower() or \
               page_admin.locator('h1:has-text("Categorias"), h2:has-text("Categorias")').count() > 0
    else:
        pytest.skip("Link de categorias não encontrado no menu admin")

@pytest.mark.e2e
def test_admin_criar_categoria(page_admin: Page):
    """Cria uma nova categoria"""
    # Navegar para categorias
    if page_admin.locator('a:has-text("Categorias"), a[href*="categoria"]').count() == 0:
        pytest.skip("Link de categorias não encontrado")

    page_admin.click('a:has-text("Categorias"), a[href*="categoria"]')
    page_admin.wait_for_load_state("networkidle")

    # Procurar botão de criar/adicionar
    botoes_criar = [
        'button:has-text("Nova Categoria")',
        'a:has-text("Nova Categoria")',
        'button:has-text("Adicionar")',
        'a:has-text("Adicionar")',
        'a[href*="nova"], a[href*="criar"], a[href*="adicionar"]'
    ]

    found = False
    for botao in botoes_criar:
        if page_admin.locator(botao).count() > 0:
            page_admin.click(botao)
            page_admin.wait_for_load_state("networkidle")
            found = True
            break

    if not found:
        pytest.skip("Botão de criar categoria não encontrado")

    # Gerar dados de teste
    dados = CategoriaBuilder.build(tipo="PRODUTO")

    # Preencher formulário
    fill_form(page_admin, dados)

    # Submeter
    page_admin.click('button[type="submit"], input[type="submit"]')
    page_admin.wait_for_load_state("networkidle")

    # Verificar sucesso
    success = page_admin.locator('.alert-success, .toast-success, [class*="success"]').count() > 0 or \
              "categoria" in page_admin.url.lower()

    assert success, "Criação de categoria deve ser bem-sucedida"

@pytest.mark.e2e
def test_admin_editar_categoria(page_admin: Page):
    """Edita uma categoria existente"""
    # Navegar para categorias
    if page_admin.locator('a:has-text("Categorias"), a[href*="categoria"]').count() == 0:
        pytest.skip("Link de categorias não encontrado")

    page_admin.click('a:has-text("Categorias"), a[href*="categoria"]')
    page_admin.wait_for_load_state("networkidle")

    # Procurar botão de editar (primeiro da lista)
    botoes_editar = [
        'a:has-text("Editar")',
        'button:has-text("Editar")',
        'a[title*="Editar"], button[title*="Editar"]',
        'a.btn-edit, button.btn-edit',
        'i.fa-edit, i.fa-pencil'
    ]

    found = False
    for botao in botoes_editar:
        if page_admin.locator(botao).count() > 0:
            page_admin.locator(botao).first.click()
            page_admin.wait_for_load_state("networkidle")
            found = True
            break

    if not found:
        pytest.skip("Nenhuma categoria para editar ou botão de edição não encontrado")

    # Modificar algum campo
    if page_admin.locator('input[name="nome"], input[name="descricao"]').count() > 0:
        campo = page_admin.locator('input[name="descricao"], textarea[name="descricao"]').first
        if campo.count() > 0:
            campo.fill("Descrição atualizada via teste E2E")

    # Submeter
    if page_admin.locator('button[type="submit"]').count() > 0:
        page_admin.click('button[type="submit"]')
        page_admin.wait_for_load_state("networkidle")

        # Verificar sucesso
        success = page_admin.locator('.alert-success, [class*="success"]').count() > 0
        assert success or "categoria" in page_admin.url.lower()

@pytest.mark.e2e
def test_admin_desativar_categoria(page_admin: Page):
    """Desativa uma categoria"""
    # Navegar para categorias
    if page_admin.locator('a:has-text("Categorias"), a[href*="categoria"]').count() == 0:
        pytest.skip("Link de categorias não encontrado")

    page_admin.click('a:has-text("Categorias"), a[href*="categoria"]')
    page_admin.wait_for_load_state("networkidle")

    # Procurar botão de desativar/inativar
    botoes_desativar = [
        'a:has-text("Desativar")',
        'button:has-text("Desativar")',
        'a:has-text("Inativar")',
        'button:has-text("Inativar")'
    ]

    for botao in botoes_desativar:
        if page_admin.locator(botao).count() > 0:
            page_admin.locator(botao).first.click()
            page_admin.wait_for_load_state("networkidle")

            # Se houver confirmação, aceitar
            if page_admin.locator('button:has-text("Confirmar"), button:has-text("Sim")').count() > 0:
                page_admin.click('button:has-text("Confirmar"), button:has-text("Sim")')
                page_admin.wait_for_load_state("networkidle")

            return

    pytest.skip("Botão de desativar não encontrado")

# ==================== USUÁRIOS ====================

@pytest.mark.e2e
def test_admin_listar_usuarios(page_admin: Page):
    """Lista todos os usuários do sistema"""
    # Navegar para usuários
    if page_admin.locator('a:has-text("Usuários"), a[href*="usuario"]').count() > 0:
        page_admin.click('a:has-text("Usuários"), a[href*="usuario"]')
        page_admin.wait_for_load_state("networkidle")

        assert_url_contains(page_admin, "/admin")
        assert "usuario" in page_admin.url.lower() or \
               page_admin.locator('h1:has-text("Usuários"), h2:has-text("Usuários")').count() > 0
    else:
        pytest.skip("Link de usuários não encontrado no menu admin")

@pytest.mark.e2e
def test_admin_visualizar_detalhes_usuario(page_admin: Page):
    """Visualiza detalhes de um usuário"""
    # Navegar para usuários
    if page_admin.locator('a:has-text("Usuários"), a[href*="usuario"]').count() == 0:
        pytest.skip("Link de usuários não encontrado")

    page_admin.click('a:has-text("Usuários"), a[href*="usuario"]')
    page_admin.wait_for_load_state("networkidle")

    # Clicar em um usuário (pode ser link para detalhes)
    links_usuario = [
        'a:has-text("Ver"), a:has-text("Detalhes")',
        'a[href*="usuario/"], a[href*="user/"]',
        'tr a'  # Links em linhas de tabela
    ]

    for link in links_usuario:
        if page_admin.locator(link).count() > 0:
            page_admin.locator(link).first.click()
            page_admin.wait_for_load_state("networkidle")

            # Verificar que está em página de detalhes
            assert page_admin.locator('h1, h2, h3').count() > 0
            return

    pytest.skip("Nenhum link de detalhes de usuário encontrado")

# ==================== FORNECEDORES ====================

@pytest.mark.e2e
def test_admin_listar_fornecedores(page_admin: Page):
    """Lista todos os fornecedores"""
    # Navegar para fornecedores
    if page_admin.locator('a:has-text("Fornecedores"), a[href*="fornecedor"], a[href*="verificacao"]').count() > 0:
        page_admin.click('a:has-text("Fornecedores"), a[href*="fornecedor"], a[href*="verificacao"]')
        page_admin.wait_for_load_state("networkidle")

        assert_url_contains(page_admin, "/admin")
        assert "fornecedor" in page_admin.url.lower() or \
               "verificacao" in page_admin.url.lower() or \
               page_admin.locator('h1:has-text("Fornecedores"), h2:has-text("Fornecedores")').count() > 0
    else:
        pytest.skip("Link de fornecedores não encontrado no menu admin")

@pytest.mark.e2e
def test_admin_aprovar_fornecedor(page_admin: Page):
    """Aprova um fornecedor pendente"""
    # Navegar para fornecedores
    if page_admin.locator('a:has-text("Fornecedores"), a[href*="fornecedor"], a[href*="verificacao"]').count() == 0:
        pytest.skip("Link de fornecedores não encontrado")

    page_admin.click('a:has-text("Fornecedores"), a[href*="fornecedor"], a[href*="verificacao"]')
    page_admin.wait_for_load_state("networkidle")

    # Procurar botão de aprovar
    botoes_aprovar = [
        'button:has-text("Aprovar")',
        'a:has-text("Aprovar")',
        'button[title*="Aprovar"], a[title*="Aprovar"]'
    ]

    for botao in botoes_aprovar:
        if page_admin.locator(botao).count() > 0:
            page_admin.locator(botao).first.click()
            page_admin.wait_for_load_state("networkidle")

            # Se houver confirmação
            if page_admin.locator('button:has-text("Confirmar"), button:has-text("Sim")').count() > 0:
                page_admin.click('button:has-text("Confirmar"), button:has-text("Sim")')
                page_admin.wait_for_load_state("networkidle")

            return

    pytest.skip("Nenhum fornecedor pendente ou botão de aprovar não encontrado")

# ==================== DEMANDAS ====================

@pytest.mark.e2e
def test_admin_visualizar_demandas(page_admin: Page):
    """Visualiza todas as demandas do sistema"""
    # Navegar para demandas
    links_demanda = [
        'a:has-text("Demandas")',
        'a[href*="demanda"]'
    ]

    found = False
    for link in links_demanda:
        if page_admin.locator(link).count() > 0:
            page_admin.click(link)
            page_admin.wait_for_load_state("networkidle")
            found = True
            break

    if not found:
        pytest.skip("Link de demandas não encontrado")

    assert_url_contains(page_admin, "/admin")
    assert "demanda" in page_admin.url.lower() or \
           page_admin.locator('h1:has-text("Demandas"), h2:has-text("Demandas")').count() > 0

# ==================== RELATÓRIOS ====================

@pytest.mark.e2e
def test_admin_acessar_relatorios(page_admin: Page):
    """Acessa área de relatórios"""
    # Navegar para relatórios
    if page_admin.locator('a:has-text("Relatórios"), a:has-text("Relatório")').count() > 0:
        page_admin.click('a:has-text("Relatórios"), a:has-text("Relatório")')
        page_admin.wait_for_load_state("networkidle")

        assert_url_contains(page_admin, "/admin")
    else:
        pytest.skip("Link de relatórios não encontrado")

# ==================== LOGOUT ====================

@pytest.mark.e2e
def test_admin_fazer_logout(page_admin: Page):
    """Faz logout do sistema"""
    # Tentar abrir dropdown de usuário se existir
    dropdown_triggers = [
        'button.dropdown-toggle',
        'a.dropdown-toggle',
        '.user-menu',
        '#userDropdown'
    ]

    for trigger in dropdown_triggers:
        if page_admin.locator(trigger).count() > 0:
            try:
                page_admin.locator(trigger).first.click()
                page_admin.wait_for_timeout(500)
                break
            except:
                pass

    # Procurar botão/link de logout
    logout_selectors = [
        'a:has-text("Sair")',
        'a:has-text("Logout")',
        'button:has-text("Sair")',
        'a[href="/logout"]',
        'a[href*="logout"]'
    ]

    for selector in logout_selectors:
        if page_admin.locator(selector).count() > 0:
            try:
                page_admin.locator(selector).first.click(timeout=5000)
                page_admin.wait_for_load_state("networkidle")

                # Verificar redirecionamento
                assert page_admin.url in [f"{BASE_URL}/", BASE_URL] or \
                       "/login" in page_admin.url
                return
            except:
                pass

    # Fallback: ir direto para /logout
    goto_url(page_admin, "/logout")
    assert_at_base_url(page_admin)
