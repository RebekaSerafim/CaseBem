"""
Exemplos de uso do serviço de e-mail MailerSend
"""
from util.email_service import (
    MailerSendService,
    EmailRecipient,
    EmailSender,
    EmailAttachment,
    enviar_email_boas_vindas,
    enviar_email_recuperacao_senha,
    enviar_notificacao_orcamento,
)
from util.email_config import EmailConfig
import base64


def exemplo_email_simples():
    """Exemplo de envio de e-mail simples"""
    print("=== Exemplo: E-mail Simples ===")

    service = MailerSendService()

    remetente = EmailSender(
        email="noreply@casebem.com.br",
        name="Case Bem"
    )

    destinatario = EmailRecipient(
        email="cliente@exemplo.com",
        name="João Silva"
    )

    resultado = service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Teste de E-mail - Case Bem",
        conteudo_html="<h1>Olá!</h1><p>Este é um e-mail de teste do Case Bem.</p>",
        conteudo_texto="Olá! Este é um e-mail de teste do Case Bem.",
        tags=["teste", "exemplo"]
    )

    print(f"Resultado: {resultado}")
    return resultado


def exemplo_email_com_anexo():
    """Exemplo de envio de e-mail com anexo"""
    print("\n=== Exemplo: E-mail com Anexo ===")

    service = MailerSendService()

    # Criar um anexo de exemplo (arquivo texto)
    conteudo_anexo = "Este é um arquivo de exemplo do Case Bem"
    conteudo_base64 = base64.b64encode(conteudo_anexo.encode()).decode()

    anexo = EmailAttachment(
        content=conteudo_base64,
        filename="exemplo_case_bem.txt",
        disposition="attachment"
    )

    remetente = EmailSender(
        email="documentos@casebem.com.br",
        name="Case Bem - Documentos"
    )

    destinatario = EmailRecipient(
        email="cliente@exemplo.com",
        name="Maria Santos"
    )

    resultado = service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Documentos do seu Casamento - Case Bem",
        conteudo_html="""
        <h2>Documentos Anexados</h2>
        <p>Olá! Seguem os documentos solicitados para o seu casamento.</p>
        <p>Confira o arquivo em anexo.</p>
        """,
        anexos=[anexo],
        tags=["documentos", "anexo"]
    )

    print(f"Resultado: {resultado}")
    return resultado


def exemplo_email_multiplos_destinatarios():
    """Exemplo de envio para múltiplos destinatários"""
    print("\n=== Exemplo: Múltiplos Destinatários ===")

    service = MailerSendService()

    remetente = EmailSender(
        email="newsletter@casebem.com.br",
        name="Case Bem - Newsletter"
    )

    destinatarios = [
        EmailRecipient(email="cliente1@exemplo.com", name="João Silva"),
        EmailRecipient(email="cliente2@exemplo.com", name="Maria Santos"),
        EmailRecipient(email="cliente3@exemplo.com", name="Pedro Costa"),
    ]

    resultado = service.enviar_email_simples(
        remetente=remetente,
        destinatarios=destinatarios,
        assunto="Newsletter Semanal - Case Bem",
        conteudo_html="""
        <h2>Newsletter Case Bem</h2>
        <p>Confira as novidades desta semana:</p>
        <ul>
            <li>Novos fornecedores cadastrados</li>
            <li>Promoções especiais</li>
            <li>Dicas para seu casamento</li>
        </ul>
        """,
        tags=["newsletter", "promocao"]
    )

    print(f"Resultado: {resultado}")
    return resultado


def exemplo_funcoes_convenientes():
    """Exemplo usando as funções de conveniência"""
    print("\n=== Exemplo: Funções de Conveniência ===")

    # E-mail de boas-vindas
    print("Enviando e-mail de boas-vindas...")
    resultado_boas_vindas = enviar_email_boas_vindas(
        email_destinatario="novo_usuario@exemplo.com",
        nome_destinatario="Ana Silva"
    )
    print(f"Boas-vindas: {resultado_boas_vindas}")

    # E-mail de recuperação de senha
    print("\nEnviando e-mail de recuperação de senha...")
    resultado_recuperacao = enviar_email_recuperacao_senha(
        email_destinatario="usuario@exemplo.com",
        nome_destinatario="Carlos Santos",
        token_reset="abc123def456ghi789"
    )
    print(f"Recuperação: {resultado_recuperacao}")

    # Notificação de orçamento
    print("\nEnviando notificação de orçamento...")
    resultado_orcamento = enviar_notificacao_orcamento(
        email_noivo="noivo@exemplo.com",
        nome_noivo="Roberto e Fernanda",
        nome_fornecedor="Buffet Delícias",
        item_nome="Buffet Completo para 100 pessoas",
        valor_orcamento=15000.00
    )
    print(f"Orçamento: {resultado_orcamento}")

    return {
        "boas_vindas": resultado_boas_vindas,
        "recuperacao": resultado_recuperacao,
        "orcamento": resultado_orcamento,
    }


def exemplo_usando_configuracoes():
    """Exemplo usando as configurações centralizadas"""
    print("\n=== Exemplo: Usando Configurações ===")

    service = MailerSendService()

    # Usar configurações do EmailConfig
    sender_config = EmailConfig.get_sender_config("support")
    remetente = EmailSender(**sender_config)

    destinatario = EmailRecipient(
        email="cliente@exemplo.com",
        name="Cliente Teste"
    )

    # Construir URL usando EmailConfig
    link_dashboard = EmailConfig.build_url("dashboard")
    link_perfil = EmailConfig.build_url("perfil", {"tab": "configuracoes"})

    # Usar tags das configurações
    tags = EmailConfig.get_tags("notificacoes")

    conteudo_html = f"""
    <h2>Atualizações da sua Conta</h2>
    <p>Olá! Confira as atualizações da sua conta no Case Bem.</p>
    <p>
        <a href="{link_dashboard}">Acessar Dashboard</a> |
        <a href="{link_perfil}">Configurar Perfil</a>
    </p>
    """

    resultado = service.enviar_email_simples(
        remetente=remetente,
        destinatarios=[destinatario],
        assunto="Atualizações da Conta - Case Bem",
        conteudo_html=conteudo_html,
        tags=tags
    )

    print(f"URLs geradas:")
    print(f"  Dashboard: {link_dashboard}")
    print(f"  Perfil: {link_perfil}")
    print(f"Tags utilizadas: {tags}")
    print(f"Resultado: {resultado}")

    return resultado


def testar_servico_completo():
    """Testa todas as funcionalidades do serviço"""
    print("🧪 TESTANDO SERVIÇO DE E-MAIL MAILERSEND 🧪")
    print("=" * 50)

    resultados = {}

    try:
        # Teste 1: E-mail simples
        resultados["simples"] = exemplo_email_simples()

        # Teste 2: E-mail com anexo
        resultados["anexo"] = exemplo_email_com_anexo()

        # Teste 3: Múltiplos destinatários
        resultados["multiplos"] = exemplo_email_multiplos_destinatarios()

        # Teste 4: Funções de conveniência
        resultados["convenientes"] = exemplo_funcoes_convenientes()

        # Teste 5: Usando configurações
        resultados["configuracoes"] = exemplo_usando_configuracoes()

        # Resumo dos resultados
        print("\n" + "=" * 50)
        print("📊 RESUMO DOS TESTES")
        print("=" * 50)

        sucessos = 0
        falhas = 0

        for nome_teste, resultado in resultados.items():
            if isinstance(resultado, dict):
                if resultado.get("sucesso"):
                    print(f"✅ {nome_teste}: SUCESSO")
                    sucessos += 1
                else:
                    print(f"❌ {nome_teste}: FALHA - {resultado.get('erro')}")
                    falhas += 1
            else:
                print(f"⚠️  {nome_teste}: Resultado não reconhecido")

        print(f"\n📈 Total: {sucessos} sucessos, {falhas} falhas")

        return resultados

    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        return {"erro": str(e)}


if __name__ == "__main__":
    # Executar todos os testes
    testar_servico_completo()