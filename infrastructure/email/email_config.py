"""
Configurações simplificadas de e-mail para o Case Bem
"""
import os


class EmailConfig:
    """Configurações centralizadas para o serviço de e-mail"""

    # Configurações básicas do remetente
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@casebem.cachoeiro.es")
    SENDER_NAME = os.getenv("SENDER_NAME", "Case Bem")

    # URL base para links nos e-mails
    BASE_URL = os.getenv("BASE_URL", "https://casebem.cachoeiro.es")

    @classmethod
    def build_url(cls, path: str, **params) -> str:
        """
        Constrói URL completa para usar em e-mails

        Args:
            path: Caminho da URL
            **params: Parâmetros de query string

        Returns:
            URL completa

        Example:
            build_url("reset-senha", token="abc123")
            # Retorna: https://casebem.cachoeiro.es/reset-senha?token=abc123
        """
        url = f"{cls.BASE_URL.rstrip('/')}/{path.lstrip('/')}"

        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url += f"?{query_string}"

        return url
