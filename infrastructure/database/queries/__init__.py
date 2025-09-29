"""
Queries SQL organizadas por domínio

Esta estrutura centraliza todas as queries SQL do sistema,
organizadas por domínio de negócio para facilitar manutenção.

Imports principais:
- base_queries: Funções utilitárias para geração de SQL
- usuario_queries: Queries do domínio de usuários e fornecedores
- categoria_queries: Queries do domínio de categorias e itens

Example:
    from infrastructure.database.queries import usuario_queries
    from infrastructure.database.queries.base_queries import gerar_select_all
"""

# Imports principais para facilitar uso
from .base_queries import (
    gerar_create_table,
    gerar_insert,
    gerar_update,
    gerar_select_all,
    gerar_select_por_id,
    gerar_delete,
    gerar_select_paginado,
    gerar_count,
    QUERIES_COMUNS
)

__all__ = [
    'gerar_create_table',
    'gerar_insert',
    'gerar_update',
    'gerar_select_all',
    'gerar_select_por_id',
    'gerar_delete',
    'gerar_select_paginado',
    'gerar_count',
    'QUERIES_COMUNS'
]