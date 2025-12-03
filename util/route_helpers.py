"""
Helpers utilitários para rotas.

Este módulo consolida funções auxiliares usadas em múltiplas rotas,
eliminando duplicação de código.
"""

from fastapi import Request


def get_active_page(request: Request, prefix: str = "") -> str:
    """
    Determina qual página está ativa baseada na URL.

    Esta função substitui get_admin_active_page, get_fornecedor_active_page
    e get_noivo_active_page que eram idênticas.

    Args:
        request: Request do FastAPI
        prefix: Prefixo da rota (ex: 'admin', 'fornecedor', 'noivo')
                Se vazio, retorna apenas a rota base

    Returns:
        str: Nome da página ativa (ex: 'dashboard', 'perfil', 'usuarios')
             ou string vazia se não houver match

    Examples:
        >>> # Para /admin/dashboard
        >>> get_active_page(request, 'admin')
        'dashboard'

        >>> # Para /fornecedor/itens
        >>> get_active_page(request, 'fornecedor')
        'itens'

        >>> # Para /noivo/demandas/nova
        >>> get_active_page(request, 'noivo')
        'demandas'
    """
    url_path = str(request.url.path)

    # Se há um prefixo, remove ele da URL
    if prefix:
        prefix_completo = f"/{prefix}/"
        if url_path.startswith(prefix_completo):
            # Remove o prefixo e pega o primeiro segmento
            rota_sem_prefixo = url_path[len(prefix_completo):]
            # Pega apenas o primeiro segmento (antes da primeira '/')
            if rota_sem_prefixo:
                primeira_parte = rota_sem_prefixo.split("/")[0]
                # Se tiver conteúdo, retorna, senão é dashboard
                return primeira_parte if primeira_parte else "dashboard"
            else:
                # URL é exatamente /prefix/ (sem mais nada)
                return "dashboard"
    else:
        # Sem prefixo, pega o primeiro segmento após a /
        partes = url_path.strip("/").split("/")
        return partes[0] if partes and partes[0] else ""

    return ""


# Funções de compatibilidade para facilitar migração gradual

def get_admin_active_page(request: Request) -> str:
    """DEPRECATED: Use get_active_page(request, 'admin')"""
    return get_active_page(request, "admin")


def get_fornecedor_active_page(request: Request) -> str:
    """DEPRECATED: Use get_active_page(request, 'fornecedor')"""
    return get_active_page(request, "fornecedor")


def get_noivo_active_page(request: Request) -> str:
    """DEPRECATED: Use get_active_page(request, 'noivo')"""
    return get_active_page(request, "noivo")


def get_public_active_page(request: Request) -> str:
    """
    Determina página ativa para rotas públicas (sem prefixo).

    DEPRECATED: Use get_active_page(request) sem prefixo
    """
    return get_active_page(request)
