"""
Infrastructure Logging - Sistema de logging estruturado

Este módulo gerencia o sistema de logging:
- logger: Logger personalizado do CaseBem
"""

from infrastructure.logging.logger import CaseBemLogger, logger

__all__ = [
    'CaseBemLogger',
    'logger',
]
