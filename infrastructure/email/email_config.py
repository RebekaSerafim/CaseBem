"""
Configurações de e-mail para o Case Bem
"""
import os
from typing import Dict, Any


class EmailConfig:
    """Configurações centralizadas para o serviço de e-mail"""

    # Configurações do remetente padrão (carregadas do .env)
    DEFAULT_SENDER_EMAIL = os.getenv("DEFAULT_SENDER_EMAIL", "noreply@casebem.com.br")
    DEFAULT_SENDER_NAME = os.getenv("DEFAULT_SENDER_NAME", "Case Bem")

    # Configurações de remetentes específicos (carregadas do .env)
    SUPPORT_SENDER_EMAIL = os.getenv("SUPPORT_SENDER_EMAIL", "suporte@casebem.com.br")
    SUPPORT_SENDER_NAME = os.getenv("SUPPORT_SENDER_NAME", "Case Bem - Suporte")

    NOTIFICATIONS_SENDER_EMAIL = os.getenv("NOTIFICATIONS_SENDER_EMAIL", "notificacoes@casebem.com.br")
    NOTIFICATIONS_SENDER_NAME = os.getenv("NOTIFICATIONS_SENDER_NAME", "Case Bem - Notificações")

    # URLs base para links nos e-mails (carregadas do .env)
    BASE_URL = os.getenv("BASE_URL", "https://casebem.com.br")
    DASHBOARD_URL = f"{BASE_URL}/dashboard"
    LOGIN_URL = f"{BASE_URL}/login"

    # Templates de e-mail (IDs do MailerSend, carregados do .env)
    TEMPLATE_IDS = {
        "boas_vindas": os.getenv("MAILERSEND_TEMPLATE_WELCOME"),
        "recuperacao_senha": os.getenv("MAILERSEND_TEMPLATE_PASSWORD_RESET"),
        "novo_orcamento": os.getenv("MAILERSEND_TEMPLATE_NEW_QUOTE"),
        "orcamento_aceito": os.getenv("MAILERSEND_TEMPLATE_QUOTE_ACCEPTED"),
        "nova_demanda": os.getenv("MAILERSEND_TEMPLATE_NEW_LEAD"),
    }

    # Tags padrão para categorização (mantidas no código)
    DEFAULT_TAGS = {
        "sistema": ["sistema", "case-bem"],
        "boas_vindas": ["boas-vindas", "novo-usuario"],
        "seguranca": ["seguranca", "autenticacao"],
        "orcamentos": ["orcamento", "negocio"],
        "notificacoes": ["notificacao", "alerta"],
    }

    # Configurações de retry e timeout (carregadas do .env)
    MAX_RETRIES = int(os.getenv("EMAIL_MAX_RETRIES", "3"))
    TIMEOUT_SECONDS = int(os.getenv("EMAIL_TIMEOUT_SECONDS", "30"))

    @classmethod
    def get_sender_config(cls, tipo: str = "default") -> Dict[str, str]:
        """
        Retorna configurações do remetente baseado no tipo

        Args:
            tipo: Tipo do remetente (default, support, notifications)

        Returns:
            Dict com email e name do remetente
        """
        configs = {
            "default": {
                "email": cls.DEFAULT_SENDER_EMAIL,
                "name": cls.DEFAULT_SENDER_NAME
            },
            "support": {
                "email": cls.SUPPORT_SENDER_EMAIL,
                "name": cls.SUPPORT_SENDER_NAME
            },
            "notifications": {
                "email": cls.NOTIFICATIONS_SENDER_EMAIL,
                "name": cls.NOTIFICATIONS_SENDER_NAME
            }
        }

        return configs.get(tipo, configs["default"])

    @classmethod
    def get_template_id(cls, template_name: str) -> str | None:
        """
        Retorna o ID do template se estiver configurado

        Args:
            template_name: Nome do template

        Returns:
            ID do template ou None se não configurado
        """
        return cls.TEMPLATE_IDS.get(template_name)

    @classmethod
    def get_tags(cls, categoria: str) -> list:
        """
        Retorna tags padrão para uma categoria

        Args:
            categoria: Categoria das tags

        Returns:
            Lista de tags
        """
        base_tags = cls.DEFAULT_TAGS.get("sistema", [])
        category_tags = cls.DEFAULT_TAGS.get(categoria, [])
        return base_tags + category_tags

    @classmethod
    def build_url(cls, path: str, params: Dict[str, Any] = {}) -> str:
        """
        Constrói URL completa para usar em e-mails

        Args:
            path: Caminho da URL
            params: Parâmetros de query string

        Returns:
            URL completa
        """
        url = f"{cls.BASE_URL.rstrip('/')}/{path.lstrip('/')}"

        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url += f"?{query_string}"

        return url


# Configurações específicas por ambiente
def get_email_settings() -> Dict[str, Any]:
    """
    Retorna configurações de e-mail baseadas nas variáveis de ambiente

    Returns:
        Dict com configurações do ambiente
    """
    # Função auxiliar para converter string do .env para boolean
    def str_to_bool(value: str) -> bool:
        return value.lower() in ('true', '1', 'yes', 'on')

    # Carrega configurações diretamente do .env
    return {
        "debug": str_to_bool(os.getenv("EMAIL_DEBUG", "true")),
        "log_emails": str_to_bool(os.getenv("EMAIL_LOG_EMAILS", "true")),
        "send_emails": str_to_bool(os.getenv("EMAIL_SEND_EMAILS", "false")),
        "fake_send": str_to_bool(os.getenv("EMAIL_FAKE_SEND", "true")),
    }


# Configurações de conteúdo de e-mail
EMAIL_STYLES = {
    "primary_color": "#28a745",
    "secondary_color": "#17a2b8",
    "danger_color": "#dc3545",
    "warning_color": "#ffc107",
    "info_color": "#17a2b8",
    "light_bg": "#f8f9fa",
    "dark_text": "#343a40",
    "muted_text": "#6c757d",
}

# Template CSS inline para e-mails
def get_email_base_styles() -> str:
    """Retorna o CSS base para e-mails formatado com as cores"""
    return f"""
    <style>
        .email-container {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
        }}
        .email-header {{
            background-color: {EMAIL_STYLES["primary_color"]};
            padding: 20px;
            text-align: center;
        }}
        .email-header h1 {{
            color: white;
            margin: 0;
            font-size: 24px;
        }}
        .email-body {{
            padding: 20px;
            line-height: 1.6;
        }}
        .email-button {{
            background-color: {EMAIL_STYLES["primary_color"]};
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            font-weight: bold;
        }}
        .email-footer {{
            background-color: {EMAIL_STYLES["light_bg"]};
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: {EMAIL_STYLES["muted_text"]};
        }}
        .highlight-box {{
            background-color: {EMAIL_STYLES["light_bg"]};
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .text-center {{
            text-align: center;
        }}
        .text-primary {{
            color: {EMAIL_STYLES["primary_color"]};
        }}
        .text-success {{
            color: {EMAIL_STYLES["primary_color"]};
        }}
        .text-danger {{
            color: {EMAIL_STYLES["danger_color"]};
        }}
        .font-weight-bold {{
            font-weight: bold;
        }}
    </style>
    """