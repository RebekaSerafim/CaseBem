"""
Pacote de utilitários do sistema CaseBem.

Este módulo contém classes e funções auxiliares usadas em todo o projeto:
- Error handlers e exception handlers
- Logger e sistema de logging
- Validações de DTOs
- Segurança e autenticação
- Utilitários de email, avatar, etc.

Uso:
    from util.exceptions import CaseBemError, ValidacaoError
    from util.logger import logger
    from util.error_handlers import tratar_erro_banco_dados
"""

# Não fazemos imports automáticos para evitar problemas com análise estática
# Cada módulo deve importar diretamente o que precisa

__all__ = [
    'exceptions',
    'logger',
    'error_handlers',
    'validacoes_dto',
    'security',
    'database',
]