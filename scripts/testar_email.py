"""
Script para testar o envio de e-mails usando Resend

Uso:
    python scripts/testar_email.py seu_email@exemplo.com

Certifique-se de configurar a variável RESEND_API_KEY no arquivo .env antes de executar.
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.email.email_service import enviar_email_boas_vindas


def testar_email(email_destinatario: str):
    """Testa o envio de e-mail de boas-vindas"""
    print(f"🔄 Testando envio de e-mail para: {email_destinatario}")
    print(f"   Usando Resend API Key: {os.getenv('RESEND_API_KEY', 'NÃO CONFIGURADA')[:10]}...")
    print()

    resultado = enviar_email_boas_vindas(
        email=email_destinatario,
        nome="Usuário Teste"
    )

    print("=" * 60)
    if resultado["sucesso"]:
        print("✅ E-mail enviado com sucesso!")
        print(f"   Message ID: {resultado.get('message_id')}")
        print()
        print("📧 Verifique sua caixa de entrada (e spam) para ver o e-mail.")
    else:
        print("❌ Falha no envio do e-mail")
        print(f"   Erro: {resultado.get('erro')}")
        print()
        print("💡 Dicas:")
        print("   1. Verifique se RESEND_API_KEY está configurada no .env")
        print("   2. Confirme que o domínio está verificado no Resend")
        print("   3. Confira se SENDER_EMAIL usa um domínio verificado")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python scripts/testar_email.py seu_email@exemplo.com")
        sys.exit(1)

    email = sys.argv[1]

    # Validação básica de e-mail
    if "@" not in email or "." not in email.split("@")[1]:
        print(f"❌ E-mail inválido: {email}")
        sys.exit(1)

    testar_email(email)
