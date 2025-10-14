"""
Serviço de envio de e-mails usando Resend
"""
import os
import resend
from typing import Optional, Dict, Any, cast
from infrastructure.logging.logger import logger


class EmailService:
    """Serviço simplificado de envio de e-mails usando Resend"""

    def __init__(self):
        """Inicializa o serviço com a API key do .env"""
        self.api_key = os.getenv("RESEND_API_KEY")
        if not self.api_key:
            raise ValueError("RESEND_API_KEY não encontrada no arquivo .env")

        resend.api_key = self.api_key

        # Configurações básicas do remetente
        self.sender_email = os.getenv("SENDER_EMAIL", "noreply@casebem.cachoeiro.es")
        self.sender_name = os.getenv("SENDER_NAME", "Case Bem")
        self.base_url = os.getenv("BASE_URL", "https://casebem.cachoeiro.es")

    def enviar_email(
        self,
        destinatario: str,
        assunto: str,
        html: str,
        nome_destinatario: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia um e-mail simples

        Args:
            destinatario: E-mail do destinatário
            assunto: Assunto do e-mail
            html: Conteúdo HTML do e-mail
            nome_destinatario: Nome do destinatário (opcional)

        Returns:
            Dict com o resultado do envio
        """
        try:
            params: Dict[str, Any] = {
                "from": f"{self.sender_name} <{self.sender_email}>",
                "to": [destinatario] if not nome_destinatario else [f"{nome_destinatario} <{destinatario}>"],
                "subject": assunto,
                "html": html
            }

            response = cast(Dict[str, Any], resend.Emails.send(params))  # type: ignore[arg-type]

            logger.info("Email enviado com sucesso",
                       destinatario=destinatario,
                       assunto=assunto,
                       message_id=response.get("id"))

            return {
                "sucesso": True,
                "message_id": response.get("id"),
                "data": response
            }

        except Exception as e:
            logger.error("Erro ao enviar e-mail",
                        destinatario=destinatario,
                        assunto=assunto,
                        erro=e)

            return {
                "sucesso": False,
                "erro": str(e),
                "data": None
            }

    def _criar_html_base(self, conteudo: str, titulo: str = "Case Bem") -> str:
        """
        Cria um HTML base para e-mails com estilo consistente

        Args:
            conteudo: Conteúdo principal do e-mail
            titulo: Título do e-mail

        Returns:
            HTML completo formatado
        """
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titulo}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background-color: #28a745; padding: 30px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px;">Case Bem</h1>
                                </td>
                            </tr>
                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px 30px;">
                                    {conteudo}
                                </td>
                            </tr>
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                                    <p style="margin: 0; color: #6c757d; font-size: 12px;">
                                        Case Bem - Conectando sonhos, criando memórias
                                    </p>
                                    <p style="margin: 5px 0 0 0; color: #6c757d; font-size: 12px;">
                                        Cachoeiro de Itapemirim - ES
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """


# Instância global do serviço
_email_service_instance = None

def get_email_service() -> EmailService:
    """Retorna a instância global do serviço de e-mail"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance


# Funções de conveniência para tipos específicos de e-mail
def enviar_email_boas_vindas(email: str, nome: str) -> Dict[str, Any]:
    """
    Envia e-mail de boas-vindas para novos usuários

    Args:
        email: E-mail do destinatário
        nome: Nome do destinatário

    Returns:
        Dict com o resultado do envio
    """
    service = get_email_service()

    conteudo = f"""
    <h2 style="color: #28a745; margin-top: 0;">Bem-vindo(a) ao Case Bem! 💒</h2>
    <p style="font-size: 16px; color: #343a40; line-height: 1.6;">
        Olá, <strong>{nome}</strong>!
    </p>
    <p style="font-size: 16px; color: #343a40; line-height: 1.6;">
        É com grande alegria que damos as boas-vindas ao Case Bem,
        a plataforma que conecta casais aos melhores fornecedores para seu casamento dos sonhos.
    </p>
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
        <p style="margin: 0; font-size: 16px; color: #343a40;"><strong>Agora você pode:</strong></p>
        <ul style="margin: 10px 0; padding-left: 20px; color: #343a40;">
            <li style="margin: 5px 0;">Navegar por diversos fornecedores especializados</li>
            <li style="margin: 5px 0;">Solicitar orçamentos personalizados</li>
            <li style="margin: 5px 0;">Organizar todos os detalhes do seu casamento em um só lugar</li>
            <li style="margin: 5px 0;">Acompanhar o progresso da organização do seu evento</li>
        </ul>
    </div>
    <p style="text-align: center; margin: 30px 0;">
        <a href="{service.base_url}/dashboard"
           style="display: inline-block; background-color: #28a745; color: #ffffff;
                  padding: 15px 30px; text-decoration: none; border-radius: 5px;
                  font-weight: bold; font-size: 16px;">
            Acessar Plataforma
        </a>
    </p>
    <p style="font-size: 14px; color: #6c757d; line-height: 1.6;">
        Se tiver alguma dúvida, nossa equipe está sempre pronta para ajudar!
    </p>
    <p style="font-size: 16px; color: #343a40; margin-top: 20px;">
        Com carinho,<br>
        <strong>Equipe Case Bem</strong>
    </p>
    """

    html = service._criar_html_base(conteudo, "Bem-vindo ao Case Bem")

    return service.enviar_email(
        destinatario=email,
        assunto="Bem-vindo(a) ao Case Bem! 💒",
        html=html,
        nome_destinatario=nome
    )


def enviar_email_recuperacao_senha(email: str, nome: str, token: str) -> Dict[str, Any]:
    """
    Envia e-mail para recuperação de senha

    Args:
        email: E-mail do destinatário
        nome: Nome do destinatário
        token: Token de recuperação de senha

    Returns:
        Dict com o resultado do envio
    """
    service = get_email_service()
    link_reset = f"{service.base_url}/reset-senha?token={token}"

    conteudo = f"""
    <h2 style="color: #dc3545; margin-top: 0;">Recuperação de Senha 🔐</h2>
    <p style="font-size: 16px; color: #343a40; line-height: 1.6;">
        Olá, <strong>{nome}</strong>!
    </p>
    <p style="font-size: 16px; color: #343a40; line-height: 1.6;">
        Recebemos uma solicitação para redefinir a senha da sua conta no Case Bem.
    </p>
    <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
        <p style="margin: 0; font-size: 14px; color: #856404;">
            <strong>⚠️ IMPORTANTE:</strong> Este link é válido por apenas 1 hora por questões de segurança.
        </p>
    </div>
    <p style="text-align: center; margin: 30px 0;">
        <a href="{link_reset}"
           style="display: inline-block; background-color: #dc3545; color: #ffffff;
                  padding: 15px 30px; text-decoration: none; border-radius: 5px;
                  font-weight: bold; font-size: 16px;">
            Redefinir Senha
        </a>
    </p>
    <p style="font-size: 14px; color: #6c757d; line-height: 1.6;">
        Se você não solicitou a redefinição de senha, pode ignorar este e-mail.
        Sua senha permanecerá inalterada.
    </p>
    <p style="font-size: 14px; color: #6c757d; line-height: 1.6;">
        Se o botão acima não funcionar, copie e cole este link no seu navegador:<br>
        <a href="{link_reset}" style="color: #007bff; word-break: break-all;">{link_reset}</a>
    </p>
    <p style="font-size: 16px; color: #343a40; margin-top: 20px;">
        Atenciosamente,<br>
        <strong>Equipe Case Bem</strong>
    </p>
    """

    html = service._criar_html_base(conteudo, "Recuperação de Senha")

    return service.enviar_email(
        destinatario=email,
        assunto="Recuperação de Senha - Case Bem 🔐",
        html=html,
        nome_destinatario=nome
    )


def enviar_notificacao_orcamento(
    email: str,
    nome: str,
    nome_fornecedor: str,
    item_nome: str,
    valor: float
) -> Dict[str, Any]:
    """
    Envia notificação de novo orçamento recebido

    Args:
        email: E-mail do destinatário
        nome: Nome do destinatário
        nome_fornecedor: Nome do fornecedor
        item_nome: Nome do item orçado
        valor: Valor do orçamento

    Returns:
        Dict com o resultado do envio
    """
    service = get_email_service()
    valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    conteudo = f"""
    <h2 style="color: #28a745; margin-top: 0;">Novo Orçamento Recebido! 💰</h2>
    <p style="font-size: 16px; color: #343a40; line-height: 1.6;">
        Olá, <strong>{nome}</strong>!
    </p>
    <p style="font-size: 16px; color: #343a40; line-height: 1.6;">
        Você recebeu um novo orçamento de <strong>{nome_fornecedor}</strong>!
    </p>
    <div style="background-color: #d4edda; border-left: 4px solid #28a745; padding: 20px; margin: 20px 0;">
        <p style="margin: 0 0 10px 0; font-size: 14px; color: #155724;">
            <strong>Item:</strong> {item_nome}
        </p>
        <p style="margin: 0; font-size: 20px; color: #155724;">
            <strong>Valor:</strong> {valor_formatado}
        </p>
    </div>
    <p style="text-align: center; margin: 30px 0;">
        <a href="{service.base_url}/dashboard"
           style="display: inline-block; background-color: #28a745; color: #ffffff;
                  padding: 15px 30px; text-decoration: none; border-radius: 5px;
                  font-weight: bold; font-size: 16px;">
            Ver Orçamento
        </a>
    </p>
    <p style="font-size: 14px; color: #6c757d; line-height: 1.6;">
        Acesse seu painel para revisar os detalhes completos e tomar uma decisão.
    </p>
    <p style="font-size: 16px; color: #343a40; margin-top: 20px;">
        Boa sorte com os preparativos!<br>
        <strong>Equipe Case Bem</strong>
    </p>
    """

    html = service._criar_html_base(conteudo, "Novo Orçamento")

    return service.enviar_email(
        destinatario=email,
        assunto=f"Novo orçamento de {nome_fornecedor} - Case Bem 💰",
        html=html,
        nome_destinatario=nome
    )
