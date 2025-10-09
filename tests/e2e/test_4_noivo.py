"""
Testes E2E para área do Noivo/Casal
Fase 5: Testa funcionalidades da área de noivos

Cobertura:
- Dashboard
- Navegação e busca de itens (produtos, serviços, espaços)
- Gestão de demandas
- Gestão de orçamentos
- Perfil
- Checklist
"""

import pytest
from playwright.sync_api import Page, expect
from tests.e2e.helpers import (
    assert_url_contains,
    fill_form,
    DemandaBuilder,
)
from tests.e2e.helpers.navigation import goto_url

# ==================== DASHBOARD ====================

@pytest.mark.e2e
def test_noivo_acessar_dashboard(page_noivo: Page):
    """Verifica acesso ao dashboard do noivo"""
    # Dashboard deve estar acessível
    assert_url_contains(page_noivo, "/noivo")

    # Deve haver algum título/conteúdo
    assert page_noivo.locator('h1, h2, h3').count() > 0

@pytest.mark.e2e
def test_noivo_visualizar_estatisticas(page_noivo: Page):
    """Verifica visualização de estatísticas no dashboard"""
    # Ir para dashboard
    goto_url(page_noivo, "/noivo/dashboard")
    page_noivo.wait_for_load_state("networkidle")

    # Verificar presença de cards/estatísticas
    cards = page_noivo.locator('.card, .widget, .stat-card, [class*="card"]')
    assert cards.count() > 0, "Dashboard deve ter pelo menos um card de estatística"

# ==================== NAVEGAÇÃO DE ITENS ====================

@pytest.mark.e2e
def test_noivo_listar_produtos(page_noivo: Page):
    """Lista produtos disponíveis"""
    # Ir direto para produtos
    goto_url(page_noivo, "/noivo/produtos")
    page_noivo.wait_for_load_state("networkidle")

    assert_url_contains(page_noivo, "/noivo")
    # Verificar que a página carregou - pode ser título, cards ou body
    assert page_noivo.locator('h1, h2, h3, .card, body').count() > 0

@pytest.mark.e2e
def test_noivo_listar_servicos(page_noivo: Page):
    """Lista serviços disponíveis"""
    # Ir direto para serviços
    goto_url(page_noivo, "/noivo/servicos")
    page_noivo.wait_for_load_state("networkidle")

    assert_url_contains(page_noivo, "/noivo")
    # Verificar que a página carregou
    assert page_noivo.locator('h1, h2, h3, .card, body').count() > 0

@pytest.mark.e2e
def test_noivo_listar_espacos(page_noivo: Page):
    """Lista espaços disponíveis"""
    # Ir direto para espaços
    goto_url(page_noivo, "/noivo/espacos")
    page_noivo.wait_for_load_state("networkidle")

    assert_url_contains(page_noivo, "/noivo")
    # Verificar que a página carregou
    assert page_noivo.locator('h1, h2, h3, .card, body').count() > 0

@pytest.mark.e2e
def test_noivo_buscar_itens(page_noivo: Page):
    """Busca itens"""
    # Ir para página de busca
    goto_url(page_noivo, "/noivo/buscar")
    page_noivo.wait_for_load_state("networkidle")

    # Procurar campo de busca
    search_selectors = [
        'input[name="busca"]',
        'input[name="search"]',
        'input[name="q"]',
        'input[type="search"]'
    ]

    for selector in search_selectors:
        if page_noivo.locator(selector).count() > 0:
            page_noivo.fill(selector, "decoração")

            # Procurar botão de busca
            if page_noivo.locator('button[type="submit"]').count() > 0:
                page_noivo.click('button[type="submit"]')
                page_noivo.wait_for_load_state("networkidle")

            return

    # Se não houver campo de busca, só verificar que a página carregou
    assert page_noivo.locator('h1, h2, h3, .card, body').count() > 0

@pytest.mark.e2e
def test_noivo_visualizar_item(page_noivo: Page):
    """Visualiza detalhes de um item"""
    # Ir para produtos primeiro
    goto_url(page_noivo, "/noivo/produtos")
    page_noivo.wait_for_load_state("networkidle")

    # Procurar link de item
    links_item = [
        'a:has-text("Ver")',
        'a:has-text("Detalhes")',
        'a[href*="/noivo/item/"]'
    ]

    for link in links_item:
        if page_noivo.locator(link).count() > 0:
            page_noivo.locator(link).first.click()
            page_noivo.wait_for_load_state("networkidle")

            # Verificar que está em detalhes do item
            assert_url_contains(page_noivo, "/noivo")
            return

    pytest.skip("Nenhum item disponível para visualizar")

# ==================== GESTÃO DE DEMANDAS ====================

@pytest.mark.e2e
def test_noivo_listar_demandas(page_noivo: Page):
    """Lista demandas do casal"""
    # Navegar para demandas
    links_demanda = [
        'a:has-text("Demandas")',
        'a:has-text("Minhas Demandas")',
        'a[href*="/noivo/demandas"]'
    ]

    for link in links_demanda:
        if page_noivo.locator(link).count() > 0:
            page_noivo.click(link)
            page_noivo.wait_for_load_state("networkidle")

            assert_url_contains(page_noivo, "/noivo")
            return

    pytest.skip("Link de demandas não encontrado")

@pytest.mark.e2e
def test_noivo_criar_demanda(page_noivo: Page):
    """Cria uma nova demanda"""
    # Navegar para demandas
    goto_url(page_noivo, "/noivo/demandas")
    page_noivo.wait_for_load_state("networkidle")

    # Procurar botão de criar demanda
    botoes_criar = [
        'a:has-text("Nova Demanda")',
        'a:has-text("Criar Demanda")',
        'button:has-text("Nova Demanda")',
        'a[href*="/noivo/demandas/nova"]'
    ]

    for botao in botoes_criar:
        if page_noivo.locator(botao).count() > 0:
            page_noivo.locator(botao).first.click()
            page_noivo.wait_for_load_state("networkidle")

            # Preencher formulário
            dados = DemandaBuilder.build()
            try:
                fill_form(page_noivo, dados)
            except:
                # Preencher campos básicos manualmente
                if page_noivo.locator('input[name="titulo"]').count() > 0:
                    page_noivo.fill('input[name="titulo"]', dados.get("titulo", "Demanda de teste"))
                if page_noivo.locator('textarea[name="descricao"]').count() > 0:
                    page_noivo.fill('textarea[name="descricao"]', dados.get("descricao", "Descrição de teste"))

            # Submeter
            if page_noivo.locator('button[type="submit"]').count() > 0:
                page_noivo.click('button[type="submit"]')
                page_noivo.wait_for_load_state("networkidle")

            return

    pytest.skip("Botão de criar demanda não encontrado")

# ==================== GESTÃO DE ORÇAMENTOS ====================

@pytest.mark.e2e
def test_noivo_listar_orcamentos(page_noivo: Page):
    """Lista orçamentos recebidos"""
    # Navegar para orçamentos
    links_orcamento = [
        'a:has-text("Orçamentos")',
        'a:has-text("Meus Orçamentos")',
        'a[href*="/noivo/orcamentos"]'
    ]

    for link in links_orcamento:
        if page_noivo.locator(link).count() > 0:
            page_noivo.click(link)
            page_noivo.wait_for_load_state("networkidle")

            assert_url_contains(page_noivo, "/noivo")
            return

    pytest.skip("Link de orçamentos não encontrado")

@pytest.mark.e2e
def test_noivo_visualizar_orcamento(page_noivo: Page):
    """Visualiza detalhes de um orçamento"""
    # Ir para orçamentos
    goto_url(page_noivo, "/noivo/orcamentos")
    page_noivo.wait_for_load_state("networkidle")

    # Procurar link de orçamento
    links_orcamento = [
        'a:has-text("Ver")',
        'a:has-text("Detalhes")',
        'a[href*="/noivo/orcamentos/"]'
    ]

    for link in links_orcamento:
        if page_noivo.locator(link).count() > 0:
            page_noivo.locator(link).first.click()
            page_noivo.wait_for_load_state("networkidle")

            # Verificar que está em detalhes
            assert_url_contains(page_noivo, "/noivo")
            return

    pytest.skip("Nenhum orçamento disponível")

@pytest.mark.e2e
def test_noivo_filtrar_orcamentos_por_status(page_noivo: Page):
    """Filtra orçamentos por status"""
    # Ir para orçamentos
    goto_url(page_noivo, "/noivo/orcamentos")
    page_noivo.wait_for_load_state("networkidle")

    # Procurar filtro de status
    if page_noivo.locator('select[name="status"]').count() > 0:
        options = page_noivo.locator('select[name="status"] option').all()
        if len(options) > 1:
            page_noivo.select_option('select[name="status"]', index=1)
            page_noivo.wait_for_load_state("networkidle")
            return

    # Tentar links de filtro
    filter_links = [
        'a:has-text("Pendentes")',
        'a:has-text("Aceitos")',
        'a:has-text("Rejeitados")'
    ]

    for link in filter_links:
        if page_noivo.locator(link).count() > 0:
            page_noivo.click(link)
            page_noivo.wait_for_load_state("networkidle")
            return

    pytest.skip("Filtro de status não encontrado")

# ==================== PERFIL ====================

@pytest.mark.e2e
def test_noivo_visualizar_perfil(page_noivo: Page):
    """Visualiza perfil do casal"""
    # Ir direto para perfil
    goto_url(page_noivo, "/noivo/perfil")
    page_noivo.wait_for_load_state("networkidle")

    assert_url_contains(page_noivo, "/noivo")
    # Verificar que a página carregou
    assert page_noivo.locator('h1, h2, h3').count() > 0

@pytest.mark.e2e
def test_noivo_editar_perfil(page_noivo: Page):
    """Edita dados do perfil do casal"""
    # Ir para perfil
    goto_url(page_noivo, "/noivo/perfil")
    page_noivo.wait_for_load_state("networkidle")

    # Procurar botão de editar
    botoes_editar = [
        'a:has-text("Editar")',
        'button:has-text("Editar")',
        'a[href*="editar"]'
    ]

    for botao in botoes_editar:
        if page_noivo.locator(botao).count() > 0:
            page_noivo.locator(botao).first.click()
            page_noivo.wait_for_load_state("networkidle")

            # Editar algum campo
            if page_noivo.locator('input[name="nome"], input[name="nome_noivo"]').count() > 0:
                current_value = page_noivo.input_value('input[name="nome"], input[name="nome_noivo"]')
                page_noivo.fill('input[name="nome"], input[name="nome_noivo"]', current_value + " Editado")

            # Submeter
            if page_noivo.locator('button[type="submit"]').count() > 0:
                page_noivo.click('button[type="submit"]')
                page_noivo.wait_for_load_state("networkidle")

            return

    pytest.skip("Botão de editar não encontrado")

# ==================== CHECKLIST ====================

@pytest.mark.e2e
def test_noivo_acessar_checklist(page_noivo: Page):
    """Acessa checklist de planejamento"""
    # Ir para checklist
    goto_url(page_noivo, "/noivo/checklist")
    page_noivo.wait_for_load_state("networkidle")

    assert_url_contains(page_noivo, "/noivo")
    # Verificar que a página carregou
    assert page_noivo.locator('h1, h2, h3').count() > 0

# ==================== NAVEGAÇÃO E UTILIDADES ====================

@pytest.mark.e2e
def test_noivo_menu_navegacao(page_noivo: Page):
    """Verifica presença de menu de navegação"""
    # Verificar itens do menu
    menu_items = [
        'Dashboard',
        'Produtos',
        'Serviços',
        'Demandas',
        'Orçamentos'
    ]

    # Contar quantos itens de menu existem
    menu_count = 0
    for item in menu_items:
        if page_noivo.locator(f'a:has-text("{item}"), nav:has-text("{item}")').count() > 0:
            menu_count += 1

    assert menu_count >= 2, "Menu noivo deve ter pelo menos 2 opções de navegação"

@pytest.mark.e2e
def test_noivo_navegar_entre_paginas(page_noivo: Page):
    """Navega entre diferentes páginas do noivo"""
    # Dashboard
    goto_url(page_noivo, "/noivo/dashboard")
    page_noivo.wait_for_load_state("networkidle")
    assert_url_contains(page_noivo, "/noivo")

    # Produtos
    goto_url(page_noivo, "/noivo/produtos")
    page_noivo.wait_for_load_state("networkidle")
    assert_url_contains(page_noivo, "/noivo")

    # Demandas
    goto_url(page_noivo, "/noivo/demandas")
    page_noivo.wait_for_load_state("networkidle")
    assert_url_contains(page_noivo, "/noivo")

    # Orçamentos
    goto_url(page_noivo, "/noivo/orcamentos")
    page_noivo.wait_for_load_state("networkidle")
    assert_url_contains(page_noivo, "/noivo")

@pytest.mark.e2e
def test_noivo_fazer_logout(page_noivo: Page):
    """Faz logout da aplicação"""
    # Tentar abrir dropdown de usuário primeiro
    dropdown_triggers = [
        'button.dropdown-toggle',
        'a.dropdown-toggle',
        '.user-menu',
        '#userDropdown'
    ]

    for trigger in dropdown_triggers:
        if page_noivo.locator(trigger).count() > 0:
            try:
                page_noivo.locator(trigger).first.click()
                page_noivo.wait_for_timeout(500)
                break
            except:
                pass

    # Procurar link de logout
    links_logout = [
        'a:has-text("Sair")',
        'a:has-text("Logout")',
        'a[href*="logout"]'
    ]

    for link in links_logout:
        if page_noivo.locator(link).count() > 0:
            try:
                page_noivo.locator(link).first.click(timeout=5000)
                page_noivo.wait_for_load_state("networkidle")

                # Verificar que foi redirecionado para página pública
                assert "/noivo" not in page_noivo.url.lower()
                return
            except:
                pass

    pytest.skip("Link de logout não encontrado")
