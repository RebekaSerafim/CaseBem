"""
Sistema de logging padronizado do CaseBem
"""

import logging
import json
from datetime import datetime
from typing import Optional, Any
from util.exceptions import CaseBemError


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

    def _serializar_valor(self, valor: Any) -> Any:
        """Serializa valores que não são JSON-serializáveis por padrão"""
        if isinstance(valor, datetime):
            return valor.isoformat()
        elif isinstance(valor, (tuple, list)):
            return [self._serializar_valor(v) for v in valor]
        elif isinstance(valor, dict):
            return {k: self._serializar_valor(v) for k, v in valor.items()}
        else:
            # Para outros objetos, tenta converter para string
            try:
                json.dumps(valor)
                return valor
            except (TypeError, ValueError):
                return str(valor)

    def _criar_contexto_log(self, **kwargs) -> dict:
        """Cria contexto padronizado para logs"""
        contexto_base = {
            "timestamp": datetime.now().isoformat(),
            "sistema": "casebem",
        }
        # Serializa todos os valores do kwargs
        for chave, valor in kwargs.items():
            contexto_base[chave] = self._serializar_valor(valor)
        return contexto_base

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