"""
Infrastructure E-mail - Sistema simplificado de envio de e-mails usando Resend
"""

from infrastructure.email.email_config import EmailConfig
from infrastructure.email.email_service import (
    EmailService,
    get_email_service,
    enviar_email_boas_vindas,
    enviar_email_recuperacao_senha,
    enviar_notificacao_orcamento,
)

__all__ = [
    # Config
    "EmailConfig",
    # Service
    "EmailService",
    "get_email_service",
    # Convenience functions
    "enviar_email_boas_vindas",
    "enviar_email_recuperacao_senha",
    "enviar_notificacao_orcamento",
]
