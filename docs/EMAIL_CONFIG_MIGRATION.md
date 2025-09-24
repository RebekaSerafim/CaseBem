# Migração das Configurações de E-mail para .env

## Resumo das Mudanças

As configurações de e-mail foram migradas do arquivo `util/email_config.py` para variáveis de ambiente no arquivo `.env`, seguindo boas práticas de segurança e configuração.

## Principais Alterações

### 1. Novas Variáveis de Ambiente

Foram adicionadas as seguintes variáveis no arquivo `.env`:

```bash
# URLs base
BASE_URL=https://casebem.com.br

# Configurações do remetente padrão
DEFAULT_SENDER_EMAIL=noreply@casebem.com.br
DEFAULT_SENDER_NAME=Case Bem

# Configurações de remetentes específicos
SUPPORT_SENDER_EMAIL=suporte@casebem.com.br
SUPPORT_SENDER_NAME=Case Bem - Suporte

NOTIFICATIONS_SENDER_EMAIL=notificacoes@casebem.com.br
NOTIFICATIONS_SENDER_NAME=Case Bem - Notificações

# Templates do MailerSend (IDs dos templates)
MAILERSEND_TEMPLATE_WELCOME=
MAILERSEND_TEMPLATE_PASSWORD_RESET=
MAILERSEND_TEMPLATE_NEW_QUOTE=
MAILERSEND_TEMPLATE_QUOTE_ACCEPTED=

# Configurações de retry e timeout para e-mails
EMAIL_MAX_RETRIES=3
EMAIL_TIMEOUT_SECONDS=30

# Configurações específicas por ambiente para e-mail
EMAIL_DEBUG=true
EMAIL_LOG_EMAILS=true
EMAIL_SEND_EMAILS=false
EMAIL_FAKE_SEND=true
```

### 2. Atualizações no EmailConfig

A classe `EmailConfig` foi modificada para carregar valores do `.env`:

```python
# Antes (valores hardcoded)
DEFAULT_SENDER_EMAIL = "noreply@casebem.com.br"

# Depois (carregado do .env)
DEFAULT_SENDER_EMAIL = os.getenv("DEFAULT_SENDER_EMAIL", "noreply@casebem.com.br")
```

### 3. Função get_email_settings() Simplificada

A função `get_email_settings()` agora carrega diretamente do `.env` ao invés de usar lógica baseada em ambiente:

```python
# Antes
def get_email_settings() -> Dict[str, Any]:
    environment = os.getenv("ENVIRONMENT", "development")
    settings = {
        "development": {...},
        "production": {...}
    }
    return settings.get(environment, settings["development"])

# Depois
def get_email_settings() -> Dict[str, Any]:
    def str_to_bool(value: str) -> bool:
        return value.lower() in ('true', '1', 'yes', 'on')

    return {
        "debug": str_to_bool(os.getenv("EMAIL_DEBUG", "true")),
        "log_emails": str_to_bool(os.getenv("EMAIL_LOG_EMAILS", "true")),
        "send_emails": str_to_bool(os.getenv("EMAIL_SEND_EMAILS", "false")),
        "fake_send": str_to_bool(os.getenv("EMAIL_FAKE_SEND", "true")),
    }
```

### 4. Atualizações no EmailService

O `util/email_service.py` foi atualizado para usar as configurações centralizadas:

```python
# Antes
remetente = EmailSender(
    email="noreply@casebem.com.br",
    name="Case Bem"
)

# Depois
sender_config = EmailConfig.get_sender_config("default")
remetente = EmailSender(
    email=sender_config["email"],
    name=sender_config["name"]
)
```

### 5. Arquivo .env.example

Foi criado um arquivo `.env.example` com todas as variáveis documentadas para facilitar a configuração em novos ambientes.

## Benefícios da Migração

1. **Segurança**: Configurações sensíveis ficam fora do código
2. **Flexibilidade**: Fácil alteração entre ambientes (dev/prod)
3. **Padrão de Mercado**: Segue o padrão 12-factor app
4. **Manutenibilidade**: Centralizadas em um local
5. **Deploy Simplificado**: Não requer alterações de código para diferentes ambientes

## Configuração para Diferentes Ambientes

### Desenvolvimento
```bash
EMAIL_SEND_EMAILS=false
EMAIL_FAKE_SEND=true
EMAIL_DEBUG=true
```

### Produção
```bash
EMAIL_SEND_EMAILS=true
EMAIL_FAKE_SEND=false
EMAIL_DEBUG=false
```

## Retrocompatibilidade

A migração mantém retrocompatibilidade através de valores padrão nos métodos `os.getenv()`. Se uma variável não estiver definida no `.env`, o sistema usará o valor padrão original.

## Como Configurar

1. Copie o arquivo `.env.example` para `.env`
2. Ajuste os valores conforme seu ambiente
3. Para produção, configure `EMAIL_SEND_EMAILS=true` e `EMAIL_FAKE_SEND=false`
4. Configure os IDs dos templates do MailerSend se estiver usando templates personalizados

## Testando a Configuração

Para verificar se as configurações estão corretas:

```python
from util.email_config import EmailConfig, get_email_settings

# Verificar configurações de remetente
print(EmailConfig.get_sender_config("default"))
print(EmailConfig.get_sender_config("support"))

# Verificar configurações de ambiente
print(get_email_settings())

# Verificar URLs
print(EmailConfig.BASE_URL)
print(EmailConfig.DASHBOARD_URL)
```