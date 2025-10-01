"""
Serviço de envio de e-mails usando MailerSend
"""
import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from mailersend import MailerSendClient, Email, EmailBuilder
from infrastructure.email.email_config import EmailConfig, get_email_settings


@dataclass
class EmailRecipient:
    """Representa um destinatário de e-mail"""
    email: str
    name: Optional[str] = None


@dataclass
class EmailSender:
    """Representa o remetente do e-mail"""
    email: str
    name: Optional[str] = None


@dataclass
class EmailAttachment:
    """Representa um anexo de e-mail"""
    content: str  # Base64 encoded content
    filename: str
    disposition: str = "attachment"  # "attachment" ou "inline"
    id: Optional[str] = None


class MailerSendService:
    """Serviço de envio de e-mails usando MailerSend"""

    def __init__(self):
        """Inicializa o serviço com a API key do .env"""
        self.api_key = os.getenv("MAILERSEND_TOKEN")
        if not self.api_key:
            raise ValueError("MAILERSEND_TOKEN não encontrado no arquivo .env")

        self.client = MailerSendClient(self.api_key)

        # Configurar Jinja2 para templates de e-mail
        self.jinja_env = Environment(
            loader=FileSystemLoader('templates/emails'),
            autoescape=True
        )

        # Carregar CSS base
        css_path = os.path.join('templates/emails', 'base_email.css')
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                self.base_css = f.read()
        except FileNotFoundError:
            self.base_css = ""

    def render_template(self, template_name: str, **context) -> str:
        """Renderiza um template de e-mail com o contexto fornecido"""
        template = self.jinja_env.get_template(template_name)
        context['base_css'] = self.base_css
        return template.render(**context)

    def enviar_email_simples(
        self,
        remetente: EmailSender,
        destinatarios: List[EmailRecipient],
        assunto: str,
        conteudo_html: str,
        conteudo_texto: Optional[str] = None,
        reply_to: Optional[EmailSender] = None,
        cc: Optional[List[EmailRecipient]] = None,
        bcc: Optional[List[EmailRecipient]] = None,
        anexos: Optional[List[EmailAttachment]] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Envia um e-mail simples

        Args:
            remetente: Dados do remetente
            destinatarios: Lista de destinatários
            assunto: Assunto do e-mail
            conteudo_html: Conteúdo HTML do e-mail
            conteudo_texto: Conteúdo texto plano (opcional)
            reply_to: E-mail para resposta (opcional)
            cc: Lista de destinatários em cópia (opcional)
            bcc: Lista de destinatários em cópia oculta (opcional)
            anexos: Lista de anexos (opcional)
            tags: Lista de tags para categorização (opcional)

        Returns:
            Dict com o resultado do envio
        """
        try:
            from mailersend import EmailContact

            # Criar o builder do e-mail
            email_builder = EmailBuilder()

            # Configurar remetente
            email_builder.from_email(
                email=remetente.email,
                name=remetente.name or remetente.email
            )

            # Configurar destinatários
            for destinatario in destinatarios:
                email_builder.to(
                    email=destinatario.email,
                    name=destinatario.name or destinatario.email
                )

            # Configurar CC se fornecido
            if cc:
                for recipient in cc:
                    email_builder.cc(
                        email=recipient.email,
                        name=recipient.name or recipient.email
                    )

            # Configurar BCC se fornecido
            if bcc:
                for recipient in bcc:
                    email_builder.bcc(
                        email=recipient.email,
                        name=recipient.name or recipient.email
                    )

            # Configurar assunto e conteúdo
            email_builder.subject(assunto)
            email_builder.html(conteudo_html)

            if conteudo_texto:
                email_builder.text(conteudo_texto)

            # Configurar reply-to se fornecido
            if reply_to:
                email_builder.reply_to(
                    email=reply_to.email,
                    name=reply_to.name or reply_to.email
                )

            # Configurar anexos se fornecidos
            if anexos:
                for anexo in anexos:
                    email_builder.attach_content(
                        content=anexo.content,
                        filename=anexo.filename
                    )

            # Configurar tags se fornecidas
            if tags:
                for tag in tags:
                    email_builder.tag(tag)

            # Construir e enviar o e-mail
            email = email_builder.build()
            response = self.client.emails.send(email)

            return {
                "sucesso": True,
                "message_id": getattr(response, 'x_message_id', None),
                "status_code": getattr(response, 'status_code', None),
                "data": response.__dict__ if hasattr(response, '__dict__') else str(response)
            }

        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e),
                "data": None
            }

    def enviar_email_template(
        self,
        remetente: EmailSender,
        destinatarios: List[EmailRecipient],
        template_id: str,
        personalizacao: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Envia um e-mail usando um template do MailerSend

        Args:
            remetente: Dados do remetente
            destinatarios: Lista de destinatários
            template_id: ID do template no MailerSend
            personalizacao: Lista de dados de personalização por destinatário
            tags: Lista de tags para categorização (opcional)

        Returns:
            Dict com o resultado do envio
        """
        try:
            from mailersend import EmailContact, EmailPersonalization

            # Criar o builder do e-mail
            email_builder = EmailBuilder()

            # Configurar remetente
            email_builder.from_email(
                email=remetente.email,
                name=remetente.name or remetente.email
            )

            # Configurar destinatários
            for destinatario in destinatarios:
                email_builder.to(
                    email=destinatario.email,
                    name=destinatario.name or destinatario.email
                )

            # Configurar template
            email_builder.template(template_id)

            # Configurar personalização se fornecida
            if personalizacao:
                for item in personalizacao:
                    email_builder.personalize(
                        email=item["email"],
                        data=item["data"]
                    )

            # Configurar tags se fornecidas
            if tags:
                for tag in tags:
                    email_builder.tag(tag)

            # Construir e enviar o e-mail
            email = email_builder.build()
            response = self.client.emails.send(email)

            return {
                "sucesso": True,
                "message_id": getattr(response, 'x_message_id', None),
                "status_code": getattr(response, 'status_code', None),
                "data": response.__dict__ if hasattr(response, '__dict__') else str(response)
            }

        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e),
                "data": None
            }

    def enviar_emails_em_lote(self, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Envia múltiplos e-mails em lote

        Args:
            emails: Lista de dicionários com dados dos e-mails

        Returns:
            Dict com o resultado do envio em lote
        """
        try:
            # Usar a API de bulk email do MailerSend
            # Nota: Esta funcionalidade requer implementação específica da biblioteca
            # Por ora, enviaremos individualmente

            resultados = []
            for email_data in emails:
                resultado = self.enviar_email_simples(**email_data)
                resultados.append(resultado)

            return {
                "sucesso": True,
                "total_emails": len(emails),
                "resultados": resultados
            }

        except Exception as e:
            return {
                "sucesso": False,
                "erro": str(e),
                "data": None
            }


# Instância global do serviço (criada sob demanda)
_email_service_instance = None

def get_email_service() -> MailerSendService:
    """Retorna a instância global do serviço de e-mail"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = MailerSendService()
    return _email_service_instance


# Funções de conveniência para uso rápido
def enviar_email_boas_vindas(email_destinatario: str, nome_destinatario: str) -> Dict[str, Any]:
    """Envia e-mail de boas-vindas para novos usuários"""
    service = get_email_service()
    sender_config = EmailConfig.get_sender_config("default")
    remetente = EmailSender(
        email=sender_config["email"],
        name=sender_config["name"]
    )

    destinatario = EmailRecipient(
        email=email_destinatario,
        name=nome_destinatario
    )

    # Renderizar template HTML
    conteudo_html = service.render_template(
        'boas_vindas.html',
        nome_destinatario=nome_destinatario,
        dashboard_url=EmailConfig.DASHBOARD_URL
    )

    # Conteúdo texto plano
    conteudo_texto = f"""
    Bem-vindo ao Case Bem!

    Olá, {nome_destinatario}!

    É com grande alegria que damos as boas-vindas ao Case Bem,
    a plataforma que conecta casais aos melhores fornecedores para seu casamento dos sonhos.

    Agora você pode:
    - Navegar por diversos fornecedores especializados
    - Solicitar orçamentos personalizados
    - Organizar todos os detalhes do seu casamento em um só lugar
    - Acompanhar o progresso da organização do seu evento

    Se tiver alguma dúvida, nossa equipe está sempre pronta para ajudar!

    Com carinho,
    Equipe Case Bem

    Case Bem - Conectando sonhos, criando memórias
    """

    return service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Bem-vindo ao Case Bem! 💒",
        conteudo_html=conteudo_html,
        conteudo_texto=conteudo_texto,
        tags=EmailConfig.get_tags("boas_vindas")
    )


def enviar_email_recuperacao_senha(email_destinatario: str, nome_destinatario: str, token_reset: str) -> Dict[str, Any]:
    """Envia e-mail para recuperação de senha"""
    service = get_email_service()
    sender_config = EmailConfig.get_sender_config("support")
    remetente = EmailSender(
        email=sender_config["email"],
        name=sender_config["name"]
    )

    destinatario = EmailRecipient(
        email=email_destinatario,
        name=nome_destinatario
    )

    link_reset = EmailConfig.build_url("reset-senha", {"token": token_reset})

    # Renderizar template HTML
    conteudo_html = service.render_template(
        'recuperacao_senha.html',
        nome_destinatario=nome_destinatario,
        link_reset=link_reset
    )

    # Conteúdo texto plano
    conteudo_texto = f"""
    Recuperação de Senha - Case Bem

    Olá, {nome_destinatario}!

    Recebemos uma solicitação para redefinir a senha da sua conta no Case Bem.

    Se você fez esta solicitação, acesse o link abaixo para criar uma nova senha:
    {link_reset}

    IMPORTANTE: Este link é válido por apenas 1 hora por questões de segurança.

    Se você não solicitou a redefinição de senha, pode ignorar este e-mail.
    Sua senha permanecerá inalterada.

    Em caso de dúvidas, entre em contato conosco.

    Atenciosamente,
    Equipe Case Bem

    Case Bem - Conectando sonhos, criando memórias
    """

    return service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Recuperação de Senha - Case Bem 🔐",
        conteudo_html=conteudo_html,
        conteudo_texto=conteudo_texto,
        tags=EmailConfig.get_tags("seguranca")
    )


def enviar_notificacao_orcamento(
    email_noivo: str,
    nome_noivo: str,
    nome_fornecedor: str,
    item_nome: str,
    valor_orcamento: float
) -> Dict[str, Any]:
    """Envia notificação de novo orçamento recebido"""
    service = get_email_service()
    sender_config = EmailConfig.get_sender_config("notifications")
    remetente = EmailSender(
        email=sender_config["email"],
        name=sender_config["name"]
    )

    destinatario = EmailRecipient(
        email=email_noivo,
        name=nome_noivo
    )

    valor_formatado = f"R$ {valor_orcamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Renderizar template HTML
    conteudo_html = service.render_template(
        'notificacao_orcamento.html',
        nome_noivo=nome_noivo,
        nome_fornecedor=nome_fornecedor,
        item_nome=item_nome,
        valor_formatado=valor_formatado,
        dashboard_url=EmailConfig.DASHBOARD_URL
    )

    return service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto=f"Novo orçamento de {nome_fornecedor} - Case Bem 💰",
        conteudo_html=conteudo_html,
        tags=EmailConfig.get_tags("orcamentos")
    )