"""
Repositórios do sistema CaseBem

Camada de acesso aos dados, implementando o padrão Repository.
Todos os repositórios herdam de BaseRepo.
"""

from core.repositories import (
    usuario_repo,
    fornecedor_repo,
    categoria_repo,
    item_repo,
    casal_repo,
    demanda_repo,
    orcamento_repo,
    chat_repo,
    favorito_repo,
    fornecedor_item_repo,
    item_demanda_repo,
    item_orcamento_repo
)

__all__ = [
    'usuario_repo',
    'fornecedor_repo',
    'categoria_repo',
    'item_repo',
    'casal_repo',
    'demanda_repo',
    'orcamento_repo',
    'chat_repo',
    'favorito_repo',
    'fornecedor_item_repo',
    'item_demanda_repo',
    'item_orcamento_repo'
]