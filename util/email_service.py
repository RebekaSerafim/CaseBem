"""
Serviço de envio de e-mails usando MailerSend
"""
import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from mailersend import MailerSendClient, Email, EmailBuilder


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
    remetente = EmailSender(
        email="noreply@casebem.com.br",
        name="Case Bem"
    )

    destinatario = EmailRecipient(
        email=email_destinatario,
        name=nome_destinatario
    )

    conteudo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; text-align: center;">
            <h1 style="color: #28a745;">Bem-vindo ao Case Bem!</h1>
        </div>

        <div style="padding: 20px;">
            <p>Olá, <strong>{nome_destinatario}</strong>!</p>

            <p>É com grande alegria que damos as boas-vindas ao <strong>Case Bem</strong>,
               a plataforma que conecta casais aos melhores fornecedores para seu casamento dos sonhos.</p>

            <p>Agora você pode:</p>
            <ul>
                <li>Navegar por diversos fornecedores especializados</li>
                <li>Solicitar orçamentos personalizados</li>
                <li>Organizar todos os detalhes do seu casamento em um só lugar</li>
                <li>Acompanhar o progresso da organização do seu evento</li>
            </ul>

            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background-color: #28a745; color: white; padding: 15px 30px;
                   text-decoration: none; border-radius: 5px; display: inline-block;">
                   Começar Agora
                </a>
            </div>

            <p>Se tiver alguma dúvida, nossa equipe está sempre pronta para ajudar!</p>

            <p>Com carinho,<br>
               <strong>Equipe Case Bem</strong></p>
        </div>

        <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
            <p>Case Bem - Conectando sonhos, criando memórias</p>
        </div>
    </body>
    </html>
    """

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

    return get_email_service().enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Bem-vindo ao Case Bem! 💒",
        conteudo_html=conteudo_html,
        conteudo_texto=conteudo_texto,
        tags=["boas-vindas", "novo-usuario"]
    )


def enviar_email_recuperacao_senha(email_destinatario: str, nome_destinatario: str, token_reset: str) -> Dict[str, Any]:
    """Envia e-mail para recuperação de senha"""
    remetente = EmailSender(
        email="noreply@casebem.com.br",
        name="Case Bem - Suporte"
    )

    destinatario = EmailRecipient(
        email=email_destinatario,
        name=nome_destinatario
    )

    link_reset = f"https://casebem.com.br/reset-senha?token={token_reset}"

    conteudo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #dc3545; padding: 20px; text-align: center;">
            <h1 style="color: white;">Recuperação de Senha</h1>
        </div>

        <div style="padding: 20px;">
            <p>Olá, <strong>{nome_destinatario}</strong>!</p>

            <p>Recebemos uma solicitação para redefinir a senha da sua conta no Case Bem.</p>

            <p>Se você fez esta solicitação, clique no botão abaixo para criar uma nova senha:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{link_reset}" style="background-color: #dc3545; color: white; padding: 15px 30px;
                   text-decoration: none; border-radius: 5px; display: inline-block;">
                   Redefinir Senha
                </a>
            </div>

            <p><strong>Importante:</strong> Este link é válido por apenas 1 hora por questões de segurança.</p>

            <p>Se você não solicitou a redefinição de senha, pode ignorar este e-mail.
               Sua senha permanecerá inalterada.</p>

            <p>Em caso de dúvidas, entre em contato conosco.</p>

            <p>Atenciosamente,<br>
               <strong>Equipe Case Bem</strong></p>
        </div>

        <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
            <p>Case Bem - Conectando sonhos, criando memórias</p>
        </div>
    </body>
    </html>
    """

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

    return get_email_service().enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Recuperação de Senha - Case Bem 🔐",
        conteudo_html=conteudo_html,
        conteudo_texto=conteudo_texto,
        tags=["recuperacao-senha", "seguranca"]
    )


def enviar_notificacao_orcamento(
    email_noivo: str,
    nome_noivo: str,
    nome_fornecedor: str,
    item_nome: str,
    valor_orcamento: float
) -> Dict[str, Any]:
    """Envia notificação de novo orçamento recebido"""
    remetente = EmailSender(
        email="noreply@casebem.com.br",
        name="Case Bem - Notificações"
    )

    destinatario = EmailRecipient(
        email=email_noivo,
        name=nome_noivo
    )

    valor_formatado = f"R$ {valor_orcamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    conteudo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #17a2b8; padding: 20px; text-align: center;">
            <h1 style="color: white;">Novo Orçamento Recebido! 💰</h1>
        </div>

        <div style="padding: 20px;">
            <p>Olá, <strong>{nome_noivo}</strong>!</p>

            <p>Temos uma ótima notícia! Você recebeu um novo orçamento para seu casamento.</p>

            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Fornecedor:</strong> {nome_fornecedor}</p>
                <p><strong>Item/Serviço:</strong> {item_nome}</p>
                <p><strong>Valor:</strong> <span style="color: #28a745; font-size: 18px; font-weight: bold;">{valor_formatado}</span></p>
            </div>

            <p>Agora você pode:</p>
            <ul>
                <li>Revisar os detalhes completos do orçamento</li>
                <li>Aceitar ou negociar a proposta</li>
                <li>Entrar em contato direto com o fornecedor</li>
                <li>Comparar com outros orçamentos</li>
            </ul>

            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background-color: #17a2b8; color: white; padding: 15px 30px;
                   text-decoration: none; border-radius: 5px; display: inline-block;">
                   Ver Orçamento
                </a>
            </div>

            <p>Não perca tempo! Os melhores fornecedores têm agenda limitada.</p>

            <p>Boa sorte com os preparativos do seu casamento!</p>

            <p>Com carinho,<br>
               <strong>Equipe Case Bem</strong></p>
        </div>

        <div style="background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
            <p>Case Bem - Conectando sonhos, criando memórias</p>
        </div>
    </body>
    </html>
    """

    return get_email_service().enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto=f"Novo orçamento de {nome_fornecedor} - Case Bem 💰",
        conteudo_html=conteudo_html,
        tags=["orcamento", "notificacao", "noivo"]
    )