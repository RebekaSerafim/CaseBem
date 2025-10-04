"""
Infrastructure Email - Sistema de envio de e-mails

Este módulo gerencia o envio de e-mails usando MailerSend:
- email_config: Configurações centralizadas
- email_service: Serviço de envio
- email_examples: Exemplos de uso
"""

from infrastructure.email.email_config import EmailConfig, get_email_settings, EMAIL_STYLES, get_email_base_styles
from infrastructure.email.email_service import (
    MailerSendService,
    EmailRecipient,
    EmailSender,
    EmailAttachment,
    get_email_service,
    enviar_email_boas_vindas,
    enviar_email_recuperacao_senha,
    enviar_notificacao_orcamento,
)

__all__ = [
    # Config
    'EmailConfig',
    'get_email_settings',
    'EMAIL_STYLES',
    'get_email_base_styles',
    # Service
    'MailerSendService',
    'EmailRecipient',
    'EmailSender',
    'EmailAttachment',
    'get_email_service',
    # Convenience functions
    'enviar_email_boas_vindas',
    'enviar_email_recuperacao_senha',
    'enviar_notificacao_orcamento',
]
