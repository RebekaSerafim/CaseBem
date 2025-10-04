"""
Infrastructure Database - Conexões e queries de banco de dados

Este módulo gerencia toda a infraestrutura de banco de dados:
- connection: Gerenciamento de conexões SQLite
- adapters: Adaptadores customizados para tipos Python/SQLite
- queries: Todas as queries SQL organizadas por entidade
"""

from infrastructure.database.connection import obter_conexao

__all__ = [
    'obter_conexao',
]
