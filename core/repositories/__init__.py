"""
Repositórios do sistema CaseBem

Camada de acesso aos dados, implementando o padrão Repository.
Todos os repositórios herdam de BaseRepo.
"""

from core.repositories.usuario_repo import usuario_repo
from core.repositories.fornecedor_repo import fornecedor_repo
from core.repositories.categoria_repo import categoria_repo
from core.repositories.item_repo import item_repo
from core.repositories.casal_repo import casal_repo
from core.repositories.demanda_repo import demanda_repo
from core.repositories.orcamento_repo import orcamento_repo
from core.repositories.chat_repo import chat_repo
from core.repositories.item_demanda_repo import item_demanda_repo
from core.repositories.item_orcamento_repo import item_orcamento_repo

__all__ = [
    'usuario_repo',
    'fornecedor_repo',
    'categoria_repo',
    'item_repo',
    'casal_repo',
    'demanda_repo',
    'orcamento_repo',
    'chat_repo',
    'item_demanda_repo',
    'item_orcamento_repo'
]