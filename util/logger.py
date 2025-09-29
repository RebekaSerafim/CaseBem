"""
Sistema de logging padronizado do CaseBem
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from .exceptions import CaseBemError, TipoErro


class CaseBemLogger:
    """Logger personalizado para o sistema"""

    def __init__(self, nome: str = "casebem"):
        self.logger = logging.getLogger(nome)
        self._configurar_logger()

    def _configurar_logger(self):
        """Configura o logger com formato padronizado"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _criar_contexto_log(self, **kwargs) -> dict:
        """Cria contexto padronizado para logs"""
        return {
            "timestamp": datetime.now().isoformat(),
            "sistema": "casebem",
            **kwargs
        }

    def info(self, mensagem: str, **contexto):
        """Log de informação"""
        contexto_completo = self._criar_contexto_log(**contexto)
        self.logger.info(f"{mensagem} - {json.dumps(contexto_completo)}")

    def warning(self, mensagem: str, **contexto):
        """Log de aviso"""
        contexto_completo = self._criar_contexto_log(**contexto)
        self.logger.warning(f"{mensagem} - {json.dumps(contexto_completo)}")

    def error(self, mensagem: str, erro: Optional[Exception] = None, **contexto):
        """Log de erro"""
        contexto_completo = self._criar_contexto_log(**contexto)

        if isinstance(erro, CaseBemError):
            contexto_completo.update(erro.to_dict())
        elif erro:
            contexto_completo["erro_original"] = str(erro)
            contexto_completo["tipo_erro_original"] = type(erro).__name__

        self.logger.error(f"{mensagem} - {json.dumps(contexto_completo)}")

    def debug(self, mensagem: str, **contexto):
        """Log de debug"""
        contexto_completo = self._criar_contexto_log(**contexto)
        self.logger.debug(f"{mensagem} - {json.dumps(contexto_completo)}")


# Instância global do logger
logger = CaseBemLogger()