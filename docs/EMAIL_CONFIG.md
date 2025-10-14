# Configuração de E-mails - Resend

Este documento explica como configurar e usar o sistema de e-mails do Case Bem usando o Resend.

## 📋 Visão Geral

O sistema foi simplificado para usar o Resend.com, eliminando a complexidade anterior do MailerSend.

### Vantagens do Resend:
- ✅ API mais simples e intuitiva
- ✅ Configuração mínima necessária
- ✅ Excelente entregabilidade
- ✅ Templates HTML diretamente no código
- ✅ Suporte gratuito para desenvolvimento

## 🔧 Configuração

### 1. Criar conta no Resend

1. Acesse [resend.com](https://resend.com)
2. Crie uma conta gratuita
3. Verifique seu domínio (ou use o domínio de teste)

### 2. Obter API Key

1. No painel do Resend, vá em **API Keys**
2. Clique em **Create API Key**
3. Dê um nome (ex: "CaseBem Production")
4. Copie a API Key gerada

### 3. Configurar variáveis de ambiente

Edite o arquivo `.env` na raiz do projeto:

```bash
# Configurações de E-mail (Resend)
RESEND_API_KEY=re_sua_api_key_aqui
SENDER_EMAIL=noreply@casebem.cachoeiro.es
SENDER_NAME=Case Bem
BASE_URL=https://casebem.cachoeiro.es
```

**Importante:**
- `RESEND_API_KEY`: Sua API Key do Resend
- `SENDER_EMAIL`: Deve usar um domínio verificado no Resend
- `SENDER_NAME`: Nome que aparece como remetente
- `BASE_URL`: URL base da aplicação (para links nos e-mails)

### 4. Verificar domínio no Resend

Para usar um domínio personalizado (ex: `@casebem.cachoeiro.es`):

1. No painel do Resend, vá em **Domains**
2. Clique em **Add Domain**
3. Adicione seu domínio
4. Configure os registros DNS conforme instruções do Resend
5. Aguarde verificação (geralmente alguns minutos)

**Para desenvolvimento:** Você pode usar o domínio de teste `onboarding@resend.dev` sem verificação.

## 📧 Tipos de E-mail Disponíveis

O sistema oferece 3 tipos de e-mail pré-configurados:

### 1. Boas-vindas
Enviado quando um novo usuário se cadastra.

```python
from infrastructure.email.email_service import enviar_email_boas_vindas

resultado = enviar_email_boas_vindas(
    email="usuario@exemplo.com",
    nome="João Silva"
)
```

### 2. Recuperação de Senha
Enviado quando o usuário solicita redefinição de senha.

```python
from infrastructure.email.email_service import enviar_email_recuperacao_senha

resultado = enviar_email_recuperacao_senha(
    email="usuario@exemplo.com",
    nome="João Silva",
    token="abc123xyz"
)
```

### 3. Notificação de Orçamento
Enviado quando um noivo recebe um novo orçamento.

```python
from infrastructure.email.email_service import enviar_notificacao_orcamento

resultado = enviar_notificacao_orcamento(
    email="usuario@exemplo.com",
    nome="João Silva",
    nome_fornecedor="Buffet Gourmet",
    item_nome="Buffet completo para 150 pessoas",
    valor=15000.00
)
```

## 🧪 Testando

### Teste rápido via script

```bash
python scripts/testar_email.py seu_email@exemplo.com
```

Este script enviará um e-mail de boas-vindas para o endereço fornecido.

### Teste manual no código

```python
from infrastructure.email.email_service import get_email_service

service = get_email_service()

resultado = service.enviar_email(
    destinatario="teste@exemplo.com",
    assunto="Teste de E-mail",
    html="<h1>Olá!</h1><p>Este é um teste.</p>",
    nome_destinatario="Nome do Destinatário"
)

print(resultado)
```

## 🎨 Customizando E-mails

### Criar novo tipo de e-mail

Adicione uma nova função em `infrastructure/email/email_service.py`:

```python
def enviar_email_personalizado(email: str, nome: str, **kwargs) -> Dict[str, Any]:
    """Seu novo tipo de e-mail"""
    service = get_email_service()

    conteudo = f"""
    <h2>Olá, {nome}!</h2>
    <p>Seu conteúdo aqui...</p>
    """

    html = service._criar_html_base(conteudo, "Título do E-mail")

    return service.enviar_email(
        destinatario=email,
        assunto="Assunto do E-mail",
        html=html,
        nome_destinatario=nome
    )
```

### Modificar template base

O template base está no método `_criar_html_base()` da classe `EmailService`.

Edite em `infrastructure/email/email_service.py`:

```python
def _criar_html_base(self, conteudo: str, titulo: str = "Case Bem") -> str:
    # Customize o HTML base aqui
    return f"""
    <!DOCTYPE html>
    <html>
    ...seu template...
    </html>
    """
```

## 🔍 Troubleshooting

### Erro: "RESEND_API_KEY não encontrada"

**Solução:** Verifique se a variável está configurada no arquivo `.env`

```bash
# Verificar se a variável está definida
cat .env | grep RESEND_API_KEY
```

### Erro: "Invalid API key"

**Solução:**
1. Verifique se copiou a API Key corretamente (sem espaços extras)
2. Confirme que a API Key está ativa no painel do Resend
3. Tente criar uma nova API Key

### Erro: "Domain not verified"

**Solução:**
1. Use `onboarding@resend.dev` para desenvolvimento
2. Ou verifique seu domínio no painel do Resend

### E-mails não estão chegando

**Verificar:**
1. ✅ Confira a pasta de spam
2. ✅ Verifique os logs da aplicação
3. ✅ Consulte o painel do Resend > **Emails** para ver status de envio
4. ✅ Confirme que o e-mail destinatário está correto

### E-mails chegam sem formatação

**Solução:** Alguns clientes de e-mail bloqueiam CSS externo. O template atual usa apenas CSS inline, que é amplamente suportado.

## 📊 Monitoramento

### Ver e-mails enviados

1. Acesse o painel do Resend
2. Vá em **Emails**
3. Veja status de cada envio (delivered, bounced, etc.)

### Logs da aplicação

Os e-mails são logados automaticamente:

```python
# Sucesso
logger.info("E-mail enviado com sucesso", destinatario=email, message_id=id)

# Erro
logger.error("Erro ao enviar e-mail", destinatario=email, erro=e)
```

## 🆚 Comparação: Antes vs Depois

### Antes (MailerSend)
```bash
# 24 variáveis de configuração no .env
MAILERSEND_TOKEN=...
DEFAULT_SENDER_EMAIL=...
DEFAULT_SENDER_NAME=...
SUPPORT_SENDER_EMAIL=...
SUPPORT_SENDER_NAME=...
NOTIFICATIONS_SENDER_EMAIL=...
NOTIFICATIONS_SENDER_NAME=...
MAILERSEND_TEMPLATE_WELCOME=...
MAILERSEND_TEMPLATE_PASSWORD_RESET=...
MAILERSEND_TEMPLATE_NEW_QUOTE=...
MAILERSEND_TEMPLATE_QUOTE_ACCEPTED=...
MAILERSEND_TEMPLATE_NEW_LEAD=...
EMAIL_MAX_RETRIES=...
EMAIL_TIMEOUT_SECONDS=...
EMAIL_DEBUG=...
EMAIL_LOG_EMAILS=...
EMAIL_SEND_EMAILS=...
EMAIL_FAKE_SEND=...
# + mais configurações...
```

### Depois (Resend)
```bash
# Apenas 4 variáveis essenciais
RESEND_API_KEY=...
SENDER_EMAIL=...
SENDER_NAME=...
BASE_URL=...
```

**Redução:** 83% menos configurações! 🎉

## 📚 Recursos Adicionais

- [Documentação oficial do Resend](https://resend.com/docs)
- [Resend Python SDK](https://github.com/resend/resend-python)
- [Exemplos de templates HTML para e-mail](https://www.mailjet.com/resources/email-gallery/)

## ✅ Checklist de Migração

- [x] Instalar biblioteca `resend`
- [x] Reescrever `email_service.py`
- [x] Simplificar `email_config.py`
- [x] Atualizar `requirements.txt`
- [x] Simplificar variáveis do `.env`
- [ ] Configurar API Key do Resend
- [ ] Verificar domínio no Resend
- [ ] Testar envio de e-mail
- [ ] Atualizar código que usa e-mails (se necessário)
